export const HELP_DB = {
    // --- Routes Génériques ---
    'default': {
        title: 'Assistant Global AgaShop',
        description: 'AgaShop est un écosystème de gestion commerciale complet conçu pour simplifier la vie des commerçants. Notre mission est de transformer chaque donnée de vente en levier de croissance. Grâce à cette plateforme, vous pouvez piloter vos stocks, vos finances et vos équipes avec une précision chirurgicale, que vous soyez sur place ou en déplacement.',
        elements: [],
        faq: []
    },

    // --- Authentification ---
    'login': {
        title: 'Portail de Sécurité (Connexion)',
        description: 'Bienvenue sur votre espace sécurisé. Cette page est le verrou de protection de votre entreprise. Elle garantit que seuls vous et votre personnel autorisé pouvez accéder aux données sensibles de votre boutique. L\'authentification est la première étape pour assurer la confidentialité de vos transactions et de vos marges bénéficiaires.',
        elements: [
            {
                type: 'Champ',
                label: 'Nom d\'utilisateur',
                desc: 'C\'est la première moitié de votre identité unique. Votre nom d\'utilisateur est strictement personnel et, combiné à votre mot de passe, il constitue votre signature numérique exclusive sur AgaShop.'
            },
            {
                type: 'Champ',
                label: 'Mot de passe sécurisé',
                desc: 'La seconde moitié de votre identité. Le mot de passe n\'est pas qu\'un simple code, c\'est l\'élément qui, associé à votre nom d\'utilisateur, verrouille votre identité unique sur toute la plateforme.'
            },
            {
                type: 'Bouton',
                label: 'Se connecter maintenant',
                desc: 'En validant ce formulaire, vous lancez le protocole de vérification. Si vos accès sont valides, l\'application chargera instantanément les données de votre boutique pour que vous puissiez commencer à travailler.'
            },
            {
                type: 'Lien',
                label: 'Créer un nouveau compte',
                desc: 'Si vous n\'êtes pas encore membre du réseau AgaShop, ce lien vous redirigera vers le formulaire d\'inscription. C\'est le point de départ pour digitaliser votre commerce et rejoindre des milliers d\'autres entrepreneurs.'
            },
            {
                type: 'Lien',
                label: 'Mot de passe oublié',
                desc: 'En cas de perte de vos accès, cette option permet de déclencher une procédure de récupération sécurisée. Vous recevrez un lien unique par mail pour redéfinir votre mot de passe sans compromettre vos données.'
            }
        ],
        faq: [
            {
                question: 'Connexion refusée ?',
                answer: 'Assurez-vous que votre connexion internet est active. Vérifiez également que vous n\'avez pas activé les majuscules par erreur. Si le problème persiste, utilisez la fonction de récupération de mot de passe.'
            }
        ]
    },

    'register': {
        title: 'Rejoindre la Révolution Numérique',
        description: 'Félicitations pour ce premier pas vers une gestion moderne. L\'inscription sur AgaShop vous ouvre les portes d\'un suivi professionnel de vos activités. Remplissez ces informations pour générer votre identité numérique unique sur notre plateforme.',
        elements: [
            {
                type: 'Champ',
                label: 'E-mail',
                desc: 'Votre adresse de contact principale pour la sécurité, les rapports et la récupération de compte.'
            },
            {
                type: 'Champ',
                label: 'Nom d\'utilisateur',
                desc: 'Le pseudonyme qui vous identifiera sur l\'application. Choisissez un nom simple et mémorisable.'
            },
            {
                type: 'Sélecteur',
                label: 'Code Pays & Téléphone',
                desc: 'Sélectionnez votre pays (ex: Burundi +257) et saisissez votre numéro. Indispensable pour la validation de vos transactions.'
            },
            {
                type: 'Champ',
                label: 'Mot de passe',
                desc: 'Créez un rempart solide (minimum 4 caractères) pour garantir la confidentialité de vos données commerciales.'
            },
            {
                type: 'Bouton',
                label: 'SE CONNECTER',
                desc: 'Déjà membre ? Retournez sur l\'écran de connexion pour accéder à votre espace de travail.'
            }
        ],
        faq: [
            {
                question: 'Pourquoi mon numéro ?',
                answer: 'Le numéro de téléphone est utilisé pour sécuriser votre compte et permettre une communication fluide avec les administrateurs.'
            }
        ]
    },

    'otp-verification': {
        title: 'Authentification à Deux Facteurs (OTP)',
        description: 'La sécurité de vos données est notre priorité absolue. Pour confirmer que vous êtes bien le propriétaire légitime de ce compte, nous avons déclenché l\'envoi d\'un code de sécurité éphémère. Cette étape garantit l\'intégrité de votre duo d\'identité unique Nom d\'utilisateur + Mot de passe.',
        elements: [
            {
                type: 'Champ',
                label: 'Code de vérification',
                desc: 'Saisissez les 6 chiffres reçus par SMS ou e-mail. Ce code est votre clé d\'accès temporaire et hautement sécurisée.'
            },
            {
                type: 'Bouton',
                label: 'Vérifier mon identité',
                desc: 'Validez le code pour lever le verrou de sécurité et accéder à toutes les fonctionnalités de votre boutique.'
            },
            {
                type: 'Lien',
                label: 'Renvoyer un code',
                desc: 'Si vous n\'avez pas reçu le message après 60 secondes, cliquez ici pour générer instantanément un nouveau code.'
            }
        ],
        faq: [
            {
                question: 'Code non reçu ?',
                answer: 'Vérifiez vos courriers indésirables (Spams) ou assurez-vous que votre numéro de téléphone est bien celui renseigné lors de l\'inscription.'
            }
        ]
    },

    'forgot-password': {
        title: 'Récupération Sécurisée d\'Accès',
        description: 'L\'oubli est humain, la sécurité est AgaShop. Si vous avez égaré le second pilier de votre identité numérique, cette interface vous permet de restaurer votre accès sans compromettre vos données commerciales et financières.',
        elements: [
            {
                type: 'Champ',
                label: 'E-mail de récupération',
                desc: 'Saisissez l\'adresse e-mail associée à votre compte. C\'est par ce canal exclusif que vous recevrez vos instructions de réinitialisation.'
            },
            {
                type: 'Bouton',
                label: 'Envoyer les instructions',
                desc: 'Déclenchez l\'envoi du lien de secours qui vous permettra de définir un nouveau mot de passe robuste.'
            }
        ],
        faq: []
    },

    'forgot-password-success': {
        title: 'Procédure de Secours Activée',
        description: 'La porte de secours est ouverte. Nous venons de vous expédier un message contenant un lien unique et temporaire vers votre adresse de récupération.',
        elements: [
            {
                type: 'Bouton',
                label: 'Retour à la Connexion',
                desc: 'Une fois votre nouveau mot de passe défini, revenez sur cet écran pour reprendre le contrôle de votre boutique.'
            }
        ],
        faq: []
    },

    // --- Espace Boutique (Shop) ---
    'home': {
        title: 'Tableau de Bord Stratégique',
        description: 'Bienvenue sur votre centre de commandement AgaShop. Le Tableau de Bord est le cerveau de votre boutique, là où chaque donnée de vente se transforme en vision stratégique. Cet écran a été conçu pour vous offrir un contrôle total et immédiat sur les piliers de votre commerce : stocks, finances, dépenses et performances.',
        elements: [
            {
                type: 'Carte',
                label: 'Produits / Ajout produit',
                desc: 'Génerer votre catalogue. Sélectionnez des articles dans le catalogue central ou créez vos propres références. C\'est ici que vous définissez vos produits et leurs images.'
            },
            {
                type: 'Carte',
                label: 'Achats (Approvisionnements)',
                desc: 'Enregistrez vos nouvelles marchandises. En notant vos achats ici, vous augmentez votre stock et permettez au système de calculer vos futurs bénéfices.'
            },
            {
                type: 'Carte',
                label: 'Contrôle du stock (Ventes)',
                desc: 'L\'outil de génération de revenus. Saisissez ce qu\'il vous reste en rayon, et AgaShop déduit automatiquement vos ventes du jour et vos bénéfices.'
            },
            {
                type: 'Carte',
                label: 'Ventes',
                desc: 'Votre rapport d\'activité. Consultez ici l\'historique détaillé de toutes vos sorties de stock, filtré par date ou par catégorie, avec le total des revenus.'
            },
            {
                type: 'Carte',
                label: 'Dépenses',
                desc: 'Gestion des charges. Notez votre loyer, factures et salaires pour que le système puisse soustraire ces montants de vos ventes et vous donner votre bénéfice **NET**.'
            },
            {
                type: 'Carte',
                label: 'Statistiques',
                desc: 'Analyses profondes. Suivez la valeur de votre stock, vos articles les plus vendus et votre rentabilité globale sous forme de tableaux clairs.'
            },
            {
                type: 'Carte',
                label: 'Modes de paiement',
                desc: 'Votre statut de compte. Gérez votre abonnement Premium, voyez le temps restant pour votre essai gratuit et accédez aux options de paiement.'
            },
            {
                type: 'Bouton',
                label: 'Bannière Premium',
                desc: 'Accélérez votre croissance. Cliquez ici pour demander une mise à niveau vers le mode Premium et débloquer toutes les fonctions illimitées.'
            }
        ],
        faq: [
            {
                question: 'Comment faire une vente ?',
                answer: 'Contrairement à une caisse classique, utilisez le menu "Contrôle du stock". Indiquez ce qu\'il vous reste, et le système calcule le reste pour vous !'
            }
        ]
    },

    'products': {
        title: 'Gestion du Catalogue & Inventaire',
        description: 'Cet espace est dédié à la structuration de votre offre commerciale. Vous pouvez y piocher des articles dans la base de données globale d\'AgaShop ou créer vos propres produits uniques. Un catalogue bien renseigné est la clé d\'une gestion automatique réussie.',
        elements: [
            {
                type: 'Icône Étoile',
                label: 'Ajouter/Retirer à la boutique',
                desc: 'Cliquez sur l\'étoile pour intégrer un produit du catalogue central dans votre boutique. Une étoile pleine signifie que l\'article est actif dans votre stock.'
            },
            {
                type: 'Sélecteur',
                label: 'Filtres Catégorie/Sous-catégorie',
                desc: 'Organisez votre vue. Filtrez par type de produit (Alimentation, Cosmétique, etc.) pour retrouver instantanément un article précis parmi des milliers.'
            },
            {
                type: 'Bouton',
                label: 'Ajouter (Bas de page)',
                desc: 'Créez une référence inédite. Si un produit n\'existe pas dans le catalogue central, vous pouvez le créer de toutes pièces avec sa photo et son nom.'
            },
            {
                type: 'Bouton',
                label: 'Supprimer (Bas de page)',
                desc: 'Affiche un guide pour retirer des articles de votre boutique en cliquant sur leurs icônes étoilées.'
            }
        ],
        faq: [
            {
                question: 'X/Y dans le titre ?',
                answer: 'X représente le nombre de produits actifs dans votre boutique, et Y le nombre total de produits disponibles dans le catalogue global.'
            }
        ]
    },

    'sales': {
        title: 'Journal et Rapports de Ventes',
        description: 'Consultez ici l\'archive de votre succès. Cette page regroupe l\'intégralité des ventes générées lors de vos contrôles de stock. C\'est un outil d\'analyse puissant pour comprendre votre flux financier sur n\'importe quelle période choisie.',
        elements: [
            {
                type: 'Entête',
                label: 'Totals & Bénéfice',
                desc: 'Visualisation immédiate du Chiffre d\'Affaires total et du bénéfice net cumulé sur les ventes affichées.'
            },
            {
                type: 'Barre de recherche',
                label: 'Recherche par mot-clé',
                desc: 'Retrouvez une vente spécifique en tapant le nom du produit ou toute information liée à la transaction.'
            },
            {
                type: 'Bouton',
                label: 'Options (Filtres profonds)',
                desc: 'Sélectionnez une plage de dates précise pour voir vos performances sur un mois, une semaine ou un jour spécifique.'
            },
            {
                type: 'Glissement (Swipe)',
                label: 'Détails des prix',
                desc: 'Faites glisser une vente vers la droite pour voir le Prix d\'Achat Unitaire (P.A.U) et Total (P.A.T) qui ont servi au calcul du bénéfice.'
            }
        ],
        faq: [
            {
                question: 'Où est le bénéfice ?',
                answer: 'Chaque ligne de vente affiche en bleu le bénéfice généré spécifiquement par cette transaction.'
            }
        ]
    },

    'supplies': {
        title: 'Gestion des Approvisionnements',
        description: 'Ne tombez plus jamais en rupture ! Ce module vous permet d\'enregistrer chaque fois que vous ramenez de nouveaux produits de chez vos fournisseurs. Cela met à jour vos stocks et, surtout, vos prix d\'achat pour un calcul de profit toujours exact.',
        elements: [
            {
                type: 'Onglet',
                label: 'Enregistrer un achat',
                desc: 'La procédure pour ajouter du nouveau stock. Sélectionnez le produit, indiquez la quantité reçue et le prix total payé à votre fournisseur.'
            },
            {
                type: 'Onglet',
                label: 'Historique des achats',
                desc: 'Le registre de tous vos investissements passés. Utile pour suivre l\'évolution des prix de vos fournisseurs.'
            },
            {
                type: 'Glissement (Swipe)',
                label: 'Modifier / Supprimer',
                desc: 'En mode historique, glissez pour corriger une erreur de saisie ou annuler un achat enregistré par erreur.'
            },
            {
                type: 'Barre de recherche',
                label: 'Filtrage avancé',
                desc: 'Utilisez les sélecteurs de catégories pour analyser vos achats par famille de produits.'
            }
        ],
        faq: [
            {
                question: 'Impact sur le stock ?',
                answer: 'Chaque achat enregistré augmente instantanément la quantité disponible pour vos futures ventes.'
            }
        ]
    },

    'supply-product-actions': {
        title: 'Ajustement d\'Approvisionnement',
        description: 'La précision est la clé d\'une bonne gestion. Utilisez cette interface pour rectifier toute erreur commise lors de la réception de vos marchandises. Que ce soit un prix mal saisi ou une quantité erronée, vous pouvez ici rétablir la vérité sur votre stock.',
        elements: [
            { type: 'Bouton', label: 'Enregistrer modifications', desc: 'Met à jour l\'achat sélectionné et rectifie le stock en conséquence.' },
            { type: 'Bouton', label: 'Annuler cet achat', desc: 'Supprime complètement l\'entrée en stock si la livraison n\'a jamais eu lieu ou a été retournée.' }
        ],
        faq: []
    },

    'expenses': {
        title: 'Registre des Charges (Dépenses)',
        description: 'La gestion d\'une boutique ne s\'arrête pas aux ventes. Pour connaître votre richesse réelle, vous devez soustraire vos charges. Utilisez cet écran pour noter chaque franc dépensé pour le fonctionnement de votre commerce.',
        elements: [
            {
                type: 'Carte',
                label: 'Total des dépenses',
                desc: 'Le cumul de toutes vos charges sur la période actuelle. Ce montant est déduit de votre profit brut pour calculer votre bénéfice net.'
            },
            {
                type: 'Bouton',
                label: 'Plus (+) Flottant',
                desc: 'Ajoutez une nouvelle dépense. Choisissez le type (Loyer, Salaire, Divers), saisissez le montant et ajoutez une description ou un numéro de reçu.'
            },
            {
                type: 'Liste',
                label: 'Historique des charges',
                desc: 'Détail chronologique de vos sorties d\'argent. Chaque ligne peut être modifiée ou supprimée en faisant glisser (swipe).'
            }
        ],
        faq: [
            {
                question: 'Pourquoi noter le loyer ?',
                answer: 'Si vous ne notez pas vos charges, AgaShop affichera un profit théorique trop élevé. Pour la vérité comptable, chaque dépense compte !'
            }
        ]
    },

    'controls': {
        title: 'Contrôle & Validation des Ventes',
        description: 'Voici le module le plus crucial pour votre rentabilité. Le contrôle consiste à compter manuellement ce qu\'il vous reste en rayon. En saisissant cette donnée, AgaShop calcule instantanément combien d\'articles ont été vendus, génère votre chiffre d\'affaires et sécurise votre bénéfice.',
        elements: [
            {
                type: 'Liste',
                label: 'Non contrôlés',
                desc: 'La liste des articles en attente de vérification. Cliquez sur un produit pour enregistrer la quantité restante actuelle.'
            },
            {
                type: 'Liste',
                label: 'Déjà contrôlés',
                desc: 'Historique des articles vérifiés aujourd\'hui. Une icône verte confirme que la vente a été enregistrée avec succès.'
            },
            {
                type: 'Bouton',
                label: 'Horloge (Calculatrice)',
                desc: 'Outil de planification. Configurez la fréquence à laquelle vous souhaitez effectuer vos contrôles (quotidien, hebdomadaire, etc.).'
            },
            {
                type: 'Calcul automatique',
                label: 'Bénéfice affiché',
                desc: 'AgaShop vous montre en temps réel le profit attendu pour chaque produit en se basant sur la différence entre prix d\'achat et prix de vente.'
            }
        ],
        faq: [
            {
                question: 'Pourquoi contrôler ?',
                answer: 'C\'est la méthode la plus fiable pour détecter les pertes ou les erreurs. Compter le stock réel est le seul moyen de garantir la justesse de vos comptes.'
            }
        ]
    },

    'stats': {
        title: 'Analyses de Performance Globale',
        description: 'Transformez vos données en intelligence commerciale. Cette page regroupe les indicateurs clés de performance (KPI) qui vous aident à comprendre la santé réelle de votre business et à prendre des décisions stratégiques basées sur des chiffres certifiés.',
        elements: [
            {
                type: 'Carte',
                label: 'Volume Stock',
                desc: 'Le compte total de tous les articles physiquement disponibles dans votre boutique. Cliquez pour voir la répartition par catégorie.'
            },
            {
                type: 'Carte',
                label: 'Valeur et Coût du Stock',
                desc: 'Le montant total de votre trésorerie immobilisée. Indique la valeur au prix de vente et, surtout, votre investissement réel (Coût d\'achat).'
            },
            {
                type: 'Carte',
                label: 'Articles Critiques',
                desc: 'Alerte automatique sur les ruptures de stock. Liste les produits à racheter en priorité pour éviter de perdre des ventes.'
            },
            {
                type: 'Carte',
                label: 'Mes Bénéfices',
                desc: 'Votre rentabilité réelle. Ce chiffre intègre désormais le coût de vos marchandises pour vous donner un bénéfice net exact.'
            }
        ],
        faq: [
            {
                question: 'Pourquoi ces chiffres ?',
                answer: 'Les données proviennent de vos contrôles de stock et de vos enregistrements d\'achats. C\'est le reflet fidèle de votre comptabilité.'
            }
        ]
    },

    'profits': {
        title: 'Bénéfices & Rentabilité Nette',
        description: 'Pilotez votre profitabilité avec rigueur. AgaShop calcule votre bénéfice net selon la règle comptable : `Ventes - (Achats + Dépenses)`. Cette vue vous permet de voir la part réelle qui revient dans votre poche après avoir payé vos fournisseurs et vos charges d\'exploitation.',
        elements: [
            {
                type: 'Graphique',
                label: 'Répartition Donut',
                desc: 'Visualisez d\'un coup d\'œil comment votre Chiffre d\'Affaires se divise entre vos Achats (marchandises), vos Dépenses (loyer, salaires) et votre Bénéfice Net.'
            },
            {
                type: 'Graphique',
                label: 'Courbe d\'Évolution',
                desc: 'Suivez la progression de votre rentabilité sur les 6 derniers mois pour identifier vos périodes de forte croissance.'
            },
            {
                type: 'Bouton',
                label: 'Historiques',
                desc: 'Accédez au journal détaillé des bénéfices mois par mois pour une analyse approfondie et certifiée.'
            }
        ],
        faq: [
            {
                question: 'Marge vs Bénéfice ?',
                answer: 'La marge est la différence entre vente et achat. Le bénéfice net affiché ici retire en plus vos charges (loyer, etc.), c\'est votre richesse réelle.'
            }
        ]
    },

    'profits-list': {
        title: 'Journal Expert des Bénéfices',
        description: 'Ce rapport détaillé présente votre performance financière mensuelle. C\'est un document de synthèse certifié en mode lecture seule pour garantir l\'exactitude de vos archives comptables.',
        elements: [
            {
                type: 'Ligne',
                label: 'Achats / Dépenses',
                desc: 'Le détail des montants soustraits de vos ventes pour arriver au résultat net. Les achats représentent le coût de vos produits.'
            },
            {
                type: 'Valeur',
                label: 'Bénéfice Net',
                desc: 'Le chiffre final en bleu (ou rouge si perte) indiquant votre résultat comptable réel sur la période.'
            }
        ],
        faq: []
    },

    'stock-volume': {
        title: 'Analyse du Volume Physique',
        description: 'Gérez la masse de votre inventaire. Cet écran vous montre combien d\'unités vous possédez au total et comment elles sont réparties. C\'est un outil essentiel pour optimiser l\'espace dans vos rayons et entrepôts.',
        elements: [
            {
                type: 'Statistique',
                label: 'Valeur totale (Achat)',
                desc: 'L\'argent total investi dans vos produits actuellement en rayon. C\'est le capital que vous devez faire circuler.'
            },
            {
                type: 'Graphique',
                label: 'Volume par Catégorie',
                desc: 'Identifiez quelles familles de produits occupent le plus de place ou de valeur dans votre boutique.'
            },
            {
                type: 'Bouton',
                label: 'Détail par article',
                desc: 'Accédez à la liste précise des quantités restant pour chaque référence de votre catalogue.'
            }
        ],
        faq: []
    },

    'stock-volume-list': {
        title: 'Inventaire Physique Détaillé',
        description: 'La liste exhaustive de vos quantités en main. Ce rapport est en lecture seule pour assurer un suivi rigoureux de vos inventaires passés. Pour modifier une quantité, passez par le module Achats ou Contrôle de Stock.',
        elements: [
            {
                type: 'Badge',
                label: 'Code Couleur Quantité',
                desc: 'Bleu : Stock sain. Orange : Stock bas. Rouge : Rupture de stock ou stock négatif (à vérifier urgemment).'
            },
            {
                type: 'Filtre',
                label: 'Recherche & Catégorie',
                desc: 'Filtrez vos articles pour réaliser un inventaire physique rapide en rayon.'
            }
        ],
        faq: []
    },

    'active-articles': {
        title: 'Valeur Financière du Stock Actif',
        description: 'Le miroir financier de vos rayons. Cet écran valorise chaque article de votre boutique pour vous montrer le potentiel de vente total par rapport à votre investissement initial.',
        elements: [
            {
                type: 'Graphique',
                label: 'Valeur / Catégorie',
                desc: 'Découvrez quelles catégories génèrent le plus de valeur financière dans vos stocks.'
            },
            {
                type: 'Bouton',
                label: 'Historique des valeurs',
                desc: 'Détail financier par article incluant la comparaison entre valeur de vente et coût d\'achat.'
            }
        ],
        faq: []
    },

    'active-articles-list': {
        title: 'Rapport Valeur & Coût de Revient',
        description: 'L\'outil d\'audit pour commerçant expert. Ce tableau compare votre potentiel de vente (V) à votre coût d\'achat (A) pour chaque produit actif. C\'est la base du calcul de votre richesse future.',
        elements: [
            {
                type: 'Colonne',
                label: 'V : Valeur de Vente',
                desc: 'Montant total que vous encaisserez en vendant tout votre stock actuel de cet article.'
            },
            {
                type: 'Colonne',
                label: 'A : Coût d\'Achat (PAT)',
                desc: 'Montant total (en orange) que vous avez réellement payé pour acquérir ce stock. C\'est votre investissement.'
            }
        ],
        faq: []
    },

    'critical-articles': {
        title: 'Centrale d\'Alerte & Réapprovisionnement',
        description: 'Anticipez vos achats pour ne jamais rater une vente. Cet écran identifie automatiquement les produits dont les quantités sont insuffisantes par rapport à vos objectifs de vente.',
        elements: [
            {
                type: 'Indicateur',
                label: 'Articles sous le seuil',
                desc: 'Le nombre total de références qui nécessitent un rachat immédiat auprès de vos fournisseurs.'
            },
            {
                type: 'Bouton',
                label: 'Liste de rachat',
                desc: 'Le bon de commande pré-rempli des articles en rupture, prêt pour votre prochaine séance d\'achats.'
            }
        ],
        faq: []
    },

    'critical-articles-list': {
        title: 'Liste des Urgences Stock',
        description: 'Votre guide de rachat journalier. Ce rapport liste uniquement les produits en état critique, classés par urgence de réapprovisionnement.',
        elements: [
            {
                type: 'Indicateur',
                label: 'Quantité Actuelle',
                desc: 'Nombre d\'unités restantes. Si le chiffre est rouge, vous êtes déjà en rupture totale sur cet article.'
            }
        ],
        faq: []
    },

    'free-stats': {
        title: 'Aperçu Quotidien (Mode Gratuit)',
        description: 'Simplicité et efficacité pour vos premiers pas. Cette vue est conçue pour les commerçants en mode standard, offrant une visibilité immédiate sur les performances essentielles de la journée.',
        elements: [
            {
                type: 'Indicateur',
                label: 'Vente du Jour',
                desc: 'Le montant brut total des ventes encaissées aujourd\'hui. Idéal pour un suivi rapide en fin de service.'
            },
            {
                type: 'Bouton',
                label: 'Passer au Premium',
                desc: 'Libérez toute la puissance d\'AgaShop. En activant le mode Premium, vous débloquez les graphiques de bénéfices nets, la gestion des dépenses et l\'analyse des stocks.'
            }
        ],
        faq: [
            {
                question: 'Pourquoi passer au Premium ?',
                answer: 'Pour piloter votre boutique comme un pro, le Premium vous permet de voir ce qu\'il vous reste réellement en poche après déduction de vos charges.'
            }
        ]
    },

    'payment-methods': {
        title: 'Centre de Gestion des Abonnements',
        description: 'Prenez les commandes de votre croissance. Cette interface vous permet de piloter votre relation avec AgaShop, de surveiller vos périodes de gratuité et de choisir le plan qui propulsera votre commerce vers de nouveaux sommets.',
        elements: [
            {
                type: 'Bannière',
                label: 'Compte à rebours de l\'Essai',
                desc: 'Consultez ici le nombre de jours restants avant la fin de vos 3 mois de succès gratuit. Anticipez votre passage au mode Premium pour ne jamais perdre votre avance.'
            },
            {
                type: 'Bouton',
                label: 'Abonnement Mensuel/6 mois/Annuel',
                desc: 'Choisissez la formule qui convient à votre budget. Plus la durée est longue, plus vous assurez la stabilité de votre gestion.'
            },
            {
                type: 'Section',
                label: 'Avantages Premium',
                desc: 'Rappel des forces du mode Premium : statistiques illimitées, suppression totale des publicités et rapports de gestion experts.'
            }
        ],
        faq: [
            {
                question: 'Que se passe-t-il après l\'essai ?',
                answer: 'Vos données sont précieusement conservées. Il vous suffira de choisir l\'un des forfaits pour réactiver instantanément toutes les fonctions de contrôle et de vente.'
            }
        ]
    },

    // --- Admin & Agent ---
    'admin-home': {
        title: 'Centre de Commande Super-Admin',
        description: 'Bienvenue dans la tour de contrôle AgaShop. En tant qu\'administrateur, vous pilotez l\'intégralité de l\'écosystème. Cet espace est dédié à la supervision globale du réseau, à la sécurité des accès et à la configuration profonde du système pour garantir une expérience fluide à tous nos commerçants.',
        elements: [
            {
                type: 'Carte',
                label: 'Gestion Catalogue',
                desc: 'Optimisez l\'arrivée des nouveaux inscrits. Définissez ici les produits modèles et les catégories standards que les commerçants pourront importer en un clic pour démarrer leur activité.'
            },
            {
                type: 'Carte',
                label: 'Gestion des agents',
                desc: 'L\'annuaire de vos forces de terrain. Créez, modifiez ou suspendez les accès de vos agents. C\'est ici que vous gérez les permissions de ceux qui déploient AgaShop sur le terrain.'
            },
            {
                type: 'Carte',
                label: 'Gestion Boutiques',
                desc: 'Le répertoire centralisé de tous les commerces. Supervisez les abonnements, validez les périodes d\'essai et assurez-vous que chaque boutique du réseau fonctionne dans les meilleures conditions.'
            },
            {
                type: 'Carte',
                label: 'Paramètres',
                desc: 'Configuration avancée du moteur AgaShop. Gérez les variables globales du système, les taux de change ou les messages de maintenance qui s\'appliquent à l\'ensemble de la plateforme.'
            },
            {
                type: 'Carte',
                label: 'Deconnexion',
                desc: 'Protégez vos privilèges d\'administration. Fermez votre session pour garantir que personne ne puisse modifier les structures critiques du système en votre absence.'
            }
        ],
        faq: []
    },

    'agent-home': {
        title: 'Tableau de Bord de l\'Agent de Croissance',
        description: 'Bienvenue, partenaire de terrain AgaShop. Votre mission est au cœur de la modernisation du commerce. Ce tableau de bord vous offre les outils nécessaires pour enrôler les boutiques, les accompagner dans leur transformation numérique et assurer un suivi de qualité pour vos clients.',
        elements: [
            {
                type: 'Carte',
                label: 'Gestion Catalogue',
                desc: 'Accédez aux modèles de produits pour aider vos nouveaux commerçants à remplir leurs rayons numériques dès leur première minute sur l\'application.'
            },
            {
                type: 'Carte',
                label: 'Gestion Boutiques',
                desc: 'Pilotez votre portefeuille client. C\'est ici que vous créez les nouvelles boutiques, activez les versions d\'essai et suivez l\'activité des commerçants que vous accompagnez.'
            },
            {
                type: 'Carte',
                label: 'Deconnexion',
                desc: 'Sécurisez votre espace de travail. Fermez votre session après avoir finalisé vos enrôlements pour protéger les données de vos commerçants.'
            }
        ],
        faq: [
            {
                question: 'Comment enrôler ?',
                answer: 'Allez dans "Gestion Boutiques" puis créez une nouvelle fiche. N\'oubliez pas d\'activer les 3 mois d\'essai gratuit pour convaincre votre client !'
            }
        ]
    },

    'admin-shops': {
        title: 'Annuaire Centralisé des Commerces',
        description: 'L\'inventaire complet du réseau AgaShop. En tant qu\'administrateur ou agent, vous avez ici une main totale sur les fiches boutiques. Vous pouvez ajuster les informations, forcer des activations ou superviser les performances de chaque membre du réseau en temps réel.',
        elements: [
            { type: 'Bouton', label: 'Validation d\'Essai (3 mois)', desc: 'Action vitale pour nos nouveaux clients : offre la puissance d\'AgaShop sans frais pour débuter.' },
            { type: 'Bouton', label: 'Gestion d\'Abonnement', desc: 'Permet à l\'admin de paramétrer les plans longue durée (1 an, expert, etc.).' },
            { type: 'Bouton', label: 'Modification de Fiche', desc: 'Mettez à jour le nom, l\'adresse ou le contact de la boutique.' }
        ],
        faq: []
    },

    'admin-users': {
        title: 'Bastion de Gestion des Identités',
        description: 'La sécurité d\'AgaShop repose sur cette interface. Contrôlez l\'accès de chaque individu au système. Vous pouvez élever un utilisateur au rang d\'Agent, suspendre des comptes pour protection ou auditer les créations. Rappelez-vous que chaque accès est verrouillé par un duo Nom d\'utilisateur + Mot de passe unique.',
        elements: [
            { type: 'Bouton', label: 'Activation/Suspension', desc: 'Gérez l\'accès au service en temps réel pour protéger l\'intégrité des données.' },
            { type: 'Bouton', label: 'Promotion en Agent', desc: 'Identifiez vos meilleurs utilisateurs et donnez-leur les outils pour recruter à leur tour.' }
        ],
        faq: []
    },

    'manage-basic-products': {
        title: 'Laboratoire de Modèles de Produits',
        description: 'Simplifiez la vie de vos commerçants dès leur arrivée. Ici, vous créez des "bases de données types" pour différents métiers (épicerie, mode, tech). En proposant ces modèles, vous permettez aux nouveaux inscrits de démarrer leur inventaire en quelques secondes plutôt qu\'en plusieurs heures.',
        elements: [
            { type: 'Bouton', label: 'Création de Modèle', desc: 'Ajoutez un article de référence qui sera disponible pour tous les nouveaux commerçants du secteur.' },
            { type: 'Champ', label: 'Catégorisation Métier', desc: 'Classez vos modèles pour qu\'un pâtissier trouve des produits de pâtisserie dès son inscription.' }
        ],
        faq: []
    },

    'admin-settings': {
        title: 'Architecture & Configuration Système',
        description: 'Vous êtes au cœur du moteur AgaShop. Ces paramètres règlent la mécanique interne de l\'application pour l\'ensemble des utilisateurs. Toute modification ici a un impact global immédiat sur l\'expérience utilisateur et les flux financiers de la plateforme.',
        elements: [
            { type: 'Champ', label: 'Configuration Monétaire', desc: 'Ajustez les taux et arrondis monétaires pour le système de paiement.' },
            { type: 'Option', label: 'Verrouillage Maintenance', desc: 'Utile pour les mises à jour majeures, cela met le système en sommeil sécurisé pour éviter toute corruption de données.' }
        ],
        faq: []
    }
};
