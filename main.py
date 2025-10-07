import pandas as pd
import numpy as np
import torch
import pickle
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

# ========= Hyperparameter =========
BATCH_SIZE   = 64
NUM_EPOCHS   = 300
LR           = 2e-5
WEIGHT_DECAY = 1e-4
THRESH       = 0.5  # Threshold für Multi-Label Prediction
HDF_PATH     = 'data.pkl'
HDF_KEY      = 'dataset'

# ========= Modell =========
num_heroes = 72  # Max-ID + 1 (IDs sind nicht fortlaufend)
hero_embed_dim = 24

model = nn.Sequential(
    nn.Embedding(num_heroes, hero_embed_dim),
    nn.Flatten(),
    nn.Linear(12 * hero_embed_dim, 128),  # 192 == hero_embed_dim * seq_len (siehe Assert unten)
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 3),     # Logits für 3 unabhängige Labels
)

# Platzhalter; wird unten mit pos_weight ersetzt
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)#,weight_decay=WEIGHT_DECAY)

# ========= Daten laden =========
with open("data.pkl", "rb") as f:
    df = pickle.load(f)

match_ids = [block[1] for block in df]

X_list = [block[0][0] for block in df]  # Liste von int-IDs pro Sample (fixe Länge)
y_list = [block[0][1] for block in df]  # Liste/Länge 3 mit 0/1

X_train = torch.tensor(X_list, dtype=torch.long)
y_train = torch.tensor(y_list, dtype=torch.float32)


# ========= Train/Val Split =========
N = X_train.shape[0]
val_ratio = 0.1 if N >= 100 else 0.2
n_val = max(1, int(N * val_ratio))
perm = torch.randperm(N)
val_idx = perm[:n_val]
trn_idx = perm[n_val:]

X_tr, y_tr = X_train[trn_idx], y_train[trn_idx]
X_val, y_val = X_train[val_idx], y_train[val_idx]

train_ds = TensorDataset(X_tr, y_tr)
val_ds   = TensorDataset(X_val, y_val)

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, drop_last=False)
val_loader   = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, drop_last=False)

# ========= pos_weight gegen Imbalance =========
with torch.no_grad():
    pos = y_tr.sum(dim=0)                       # [3]
    neg = y_tr.shape[0] - pos
    pos_weight = (neg / pos.clamp_min(1)).to(torch.float32)  # [3]

loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# ========= Bias-Init des letzten Heads =========
last = model[-1]
if isinstance(last, nn.Linear) and last.out_features == 3:
    with torch.no_grad():
        p = (pos / (pos + neg).clamp_min(1)).clamp(1e-4, 1-1e-4)  # Grundrate je Label
        bias_init = torch.log(p / (1 - p))
        last.bias.copy_(bias_init)

# ========= Training =========
for epoch in range(1, NUM_EPOCHS + 1):
    # ---- Train ----
    model.train()
    train_loss_sum = 0.0
    for xb, yb in train_loader:
        optimizer.zero_grad(set_to_none=True)
        logits = model(xb)           # [B,3] Logits
        loss = loss_fn(logits, yb)
        loss.backward()
        optimizer.step()

        train_loss_sum += loss.item() * xb.size(0)

    train_loss = train_loss_sum / len(train_ds)

    # ---- Validation + Accuracy ----
    model.eval()
    val_loss_sum = 0.0
    total = 0

    # Zähler für Accuracy
    correct_per_label = torch.zeros(3, dtype=torch.long)
    correct_subset = 0

    with torch.inference_mode():
        for xb, yb in val_loader:
            logits = model(xb)
            loss = loss_fn(logits, yb)
            val_loss_sum += loss.item() * xb.size(0)

            probs = torch.sigmoid(logits)
            preds = (probs > THRESH).int()   # [B,3]
            y_int = (yb > 0.5).int()         # sicher auf 0/1

            # Per-Label korrekte Vorhersagen addieren
            correct_per_label += (preds == y_int).sum(dim=0)

            # Subset-Accuracy (alle 3 korrekt)
            correct_subset += (preds == y_int).all(dim=1).sum().item()

            total += xb.size(0)

    val_loss = val_loss_sum / max(1, len(val_ds))
    per_label_acc = (correct_per_label.float() / max(1, total))  # [3]
    macro_label_acc = per_label_acc.mean().item()
    subset_acc = correct_subset / max(1, total)

    print(
        f"Epoch {epoch:03d} | "
        f"train_loss: {train_loss:.4f} | "
        f"val_loss: {val_loss:.4f} | "
        f"val_acc_subset: {subset_acc:.4f} | "
        f"val_acc_per_label: {per_label_acc.tolist()} | "
        f"val_acc_macro: {macro_label_acc:.4f}"
    )

# ========= Inference (gesamter Train-Satz; optional) =========
model.eval()
with torch.inference_mode():
    logits_all = model(X_train)
    probs_all  = torch.sigmoid(logits_all)
    preds_05   = (probs_all > THRESH).int()

torch.save(model, f"models/Adam-{LR}-AQ.pth")