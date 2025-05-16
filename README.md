
<h1 align="center">🖥️ Server Multi-Check</h1>

<p align="center">
  Outil léger en Python pour effectuer des vérifications de disponibilité sur plusieurs serveurs en parallèle, via différents protocoles.
</p>

---

## 🚀 Aperçu

**Server Multi-Check** est un outil de monitoring minimaliste qui permet de vérifier la disponibilité de plusieurs serveurs en se basant sur un fichier de configuration JSON. Il prend en charge les protocoles HTTP/HTTPS et TCP, avec une architecture modulaire pensée pour l’extension facile.

---

## 📁 Structure du projet

```
server-multi-check/
├── config/          # Fichiers de configuration des serveurs
├── scripts/         # Scripts utilitaires
├── src/             # Code source principal
│   ├── checker/     # Modules de vérification (http, tcp...)
│   └── utils/       # Fonctions utilitaires (log, parsing...)
├── tests/           # Tests unitaires
├── main.py          # Point d'entrée de l'application
└── README.md        # Documentation du projet
```

---

## ⚙️ Utilisation

1. **Clone le dépôt** :

```bash
git clone https://github.com/Shiro-cha/server-multi-check.git
cd server-multi-check
```

2. **Configure tes serveurs** :

Crée ou modifie un fichier dans `config/` avec la structure suivante :

```json
{
  "servers": [
    {
      "name": "Mock Server 1",
      "ip_address": "192.168.0.10",
      "port": 8080,
      "user": "admin",
      "password": "admin123",
      "key": "mock_key_123"
    },
    {
      "name": "Mock Server 2",
      "ip_address": "10.0.0.5",
      "port": 443,
      "user": "testuser",
      "password": "securepass",
      "key": "ssh-key-string"
    }
  ]
}
```

3. **Lance le checker** :

```bash
python main.py
```

---

## ✅ Protocoles supportés

* `HTTP` / `HTTPS` : Vérifie que le serveur répond avec un code 2xx/3xx
* `TCP` : Vérifie que le port cible est ouvert (connexion socket)

---

## 🔧 Champs disponibles

| Champ        | Description                           |
| ------------ | ------------------------------------- |
| `name`       | Nom lisible du serveur                |
| `ip_address` | Adresse IP ou hostname                |
| `port`       | Port cible à tester                   |
| `user`       | (Optionnel) Nom d'utilisateur         |
| `password`   | (Optionnel) Mot de passe              |
| `key`        | (Optionnel) Clé privée ou identifiant |

---

## 🛠️ Extension possible

* Ajout de protocoles : Ping, SSH, DNS, FTP, etc.
* Intégration avec Prometheus, Grafana, ou Slack
* Interface web (FastAPI + Next.js ou React)

---

## 🤝 Contribution

Les contributions sont les bienvenues !
Fork le repo, crée une branche (`feat/ton-feature`), push et ouvre une PR. Let's build something cool together. ⚒️🔥

---

## 📜 Licence

Distribué sous licence **GPL-3.0**.
Voir [LICENSE](LICENSE) pour plus de détails.

