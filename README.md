# 🏦 Banking Transactions Dashboard - Streamlit

Application web métier pour interagir avec l'API Banking Transactions.

##  Fonctionnalités

###  Vue d'ensemble
- Statistiques globales (total transactions, taux de fraude, montant moyen)
- Graphiques de répartition par type
- Analyse de la fraude par type

### Transactions
- Filtrage par type et statut de fraude
- Recherche avancée
- Affichage tabulaire des résultats
- Statistiques rapides sur les résultats

###  Détection de Fraude
- Résumé global de la fraude
- Métriques de performance (précision, rappel)
- Analyse comparative par type de transaction

###  Clients
- Top clients par volume de transactions
- Graphiques de classement
- Recherche de profil client individuel
- Statistiques détaillées par client

### 🔮 Prédiction de Fraude
- Interface de saisie de transaction
- Prédiction en temps réel
- Jauge de risque visuelle
- Recommandations automatiques

## Installation

### Prérequis
- Python 3.12+
- L'API Banking Transactions doit être lancée sur http://localhost:8000


##  Lancement

### 1. Démarrer l'API (dans un terminal)

```bash
cd banking-transactions-api
uvicorn app.main:app --reload
```

### 2. Lancer Streamlit (dans un autre terminal)

```bash
cd banking-streamlit-app
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur sur http://localhost:8501

## 📱 Utilisation

### Navigation

Utilisez la barre latérale pour naviguer entre les différentes pages :

1. **📈 Vue d'ensemble** - Dashboard principal avec KPIs
2. **💳 Transactions** - Explorer et filtrer les transactions
3. **🚨 Détection de Fraude** - Analyser les fraudes détectées
4. **👥 Clients** - Voir les top clients et rechercher des profils
5. **🔮 Prédiction de Fraude** - Tester le modèle de prédiction

### Exemples d'Utilisation

#### Rechercher des Transactions Frauduleuses

1. Aller dans **💳 Transactions**
2. Sélectionner "Frauduleux" dans le filtre Fraude
3. Cliquer sur " Rechercher"

#### Analyser un Client

1. Aller dans **👥 Clients**
2. Descendre à "🔍 Rechercher un Client"
3. Entrer l'ID (ex: C1556)
4. Cliquer sur "Rechercher"

#### Prédire une Fraude

1. Aller dans **🔮 Prédiction de Fraude**
2. Remplir les champs :
   - Type : TRANSFER
   - Montant : 250000
   - Ancien Solde : 300000
   - Nouveau Solde : 50000
3. Cliquer sur "🎯 Prédire"

## 🎨 Captures d'écran

L'application propose :
- 📊 Graphiques interactifs (Plotly)
- 📈 KPIs en temps réel
- 🎯 Interface intuitive
- 📱 Design responsive

## 📊 Dépendances

- **streamlit** - Framework web
- **requests** - Appels API
- **pandas** - Manipulation de données
- **plotly** - Visualisations interactives


### L'API n'est pas accessible

Vérifiez que :
1. L'API est bien lancée : http://localhost:8000/docs
2. Le port 8000 n'est pas bloqué
3. L'URL dans `app.py` est correcte

### Erreur au lancement

```bash
# Réinstallez les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifiez la version de Python
python --version  # Doit être 3.12+
```

### Streamlit ne s'ouvre pas

```bash
# Lancez manuellement avec le navigateur
streamlit run app.py --server.headless=false
```

## 📝 Structure

```
banking-streamlit-app/
├── app.py              # Application principale  
└── README.md          # Ce fichier
```

## 🎓 Points Bonus

Cette application permet d'obtenir le **point bonus Streamlit** du projet :
- ✅ Application web métier séparée
- ✅ Interface complète pour tester l'API
- ✅ Visualisations graphiques
- ✅ Interactions utilisateur

## 📞 Support

En cas de problème :
1. Vérifiez que l'API fonctionne
2. Consultez la documentation Streamlit
3. Vérifiez les logs dans le terminal

---

**Développé pour le projet MBA 2 - Python**  
**Framework** : Streamlit 1.29.0  
**Compatible avec** : Banking Transactions API v1.0.0
