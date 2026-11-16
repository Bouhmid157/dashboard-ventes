import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

produits = {
    "Laptop": ("Informatique", 1800),
    "Souris": ("Accessoires", 40),
    "Clavier": ("Accessoires", 90),
    "Écran": ("Informatique", 600),
    "Casque": ("Audio", 150),
    "Enceinte": ("Audio", 200),
    "Webcam": ("Accessoires", 120),
}
villes = ["Tunis", "Sfax", "Sousse", "Bizerte", "Nabeul", "Gabès"]
clients = [f"Client {i}" for i in range(1, 81)]

noms = np.random.choice(list(produits.keys()), n)
df = pd.DataFrame({
    "date": pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 700, n), unit="D"),
    "client": np.random.choice(clients, n),
    "produit": noms,
    "categorie": [produits[p][0] for p in noms],
    "ville": np.random.choice(villes, n),
})
prix = np.array([produits[p][1] for p in noms])
quantite = np.random.randint(1, 4, n)
df["montant"] = (prix * quantite * np.random.uniform(0.9, 1.1, n)).round(0)

df.sort_values("date").to_csv("data/ventes.csv", index=False)
print(df.head())
print(f"{len(df)} lignes générées")