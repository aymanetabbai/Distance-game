from app.classes_dao.configuration import DBConnection

class InitBDDDAO :
    
    @staticmethod
    def init_bdd () -> None:
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """CREATE TABLE utilisateur (
                        username VARCHAR(255) PRIMARY KEY,
                        mot_de_passe VARCHAR(255) NOT NULL,
                        -- mot de passe hache de type str
                        date_creation_compte TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)
                    );

                    CREATE TABLE coordonnees (
                        id_coordonnees SERIAL PRIMARY KEY,
                        coordonnee_x INTEGER,
                        coordonnee_y INTEGER
                    );

                    CREATE TABLE campagne (
                        id_campagne SERIAL PRIMARY KEY,
                        nom_campagne VARCHAR(255),
                        nb_places_libres INTEGER,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)
                    );

                    -- remplace les tables joueur et maitre_jeu
                    CREATE TABLE acteur (
                        id_acteur SERIAL PRIMARY KEY,
                        username VARCHAR(255) REFERENCES utilisateur (username) ON DELETE CASCADE,
                        est_mj BOOLEAN
                    );

                    CREATE TABLE campagne_acteur(
                        id_campagne INTEGER REFERENCES campagne (id_campagne) ON DELETE CASCADE, 
                        id_acteur INTEGER REFERENCES acteur (id_acteur) ON DELETE CASCADE,
                        CONSTRAINT campagne_acteur_pkey PRIMARY KEY (id_campagne, id_acteur)
                    );

                    CREATE TABLE carte (
                        id_carte SERIAL PRIMARY KEY,
                        nom_carte VARCHAR(255),
                        id_coordonnees INTEGER REFERENCES coordonnees (id_coordonnees) ON DELETE CASCADE,
                        est_actuelle BOOLEAN DEFAULT FALSE
                    ); 

                    CREATE TABLE campagne_carte (
                        id_campagne INTEGER REFERENCES campagne (id_campagne) ON DELETE CASCADE, 
                        id_carte INTEGER REFERENCES carte (id_carte) ON DELETE CASCADE,
                        CONSTRAINT campagne_carte_pkey PRIMARY KEY (id_campagne, id_carte)
                    );

                    CREATE TABLE element (
                        id_element SERIAL PRIMARY KEY,
                        id_coordonnees INTEGER REFERENCES coordonnees (id_coordonnees),
                        id_api VARCHAR(255), 
                        est_revele BOOLEAN,
                        type_element VARCHAR(255),
                        -- 'MONSTRE' ou 'EQUIPEMENT'
                        hp_monstre INTEGER
                    );

                    CREATE TABLE carte_element (
                        id_carte INTEGER REFERENCES carte (id_carte) ON DELETE CASCADE, 
                        id_element INTEGER REFERENCES element (id_element) ON DELETE CASCADE,
                        CONSTRAINT carte_element_pkey PRIMARY KEY (id_carte, id_element)
                    );

                    CREATE TABLE personnage (
                        id_personnage SERIAL PRIMARY KEY,
                        id_acteur INTEGER REFERENCES acteur (id_acteur),
                        id_coordonnees INTEGER REFERENCES coordonnees (id_coordonnees),
                        nom_personnage VARCHAR(255),
                        id_api_race VARCHAR(255),
                        id_api_classe VARCHAR(255),
                        hp INTEGER,
                        attaque INTEGER, 
                        defense INTEGER,
                        vitesse INTEGER,
                        niveau INTEGER
                    );

                    CREATE TABLE personnage_equipement (
                        id_personnage INTEGER REFERENCES personnage (id_personnage) ON DELETE CASCADE,
                        id_equipement INTEGER REFERENCES element (id_element) ON DELETE CASCADE,
                        CONSTRAINT personnage_equipement_pkey PRIMARY KEY (id_personnage, id_equipement)
                    );

                    CREATE TABLE de (
                        id_de SERIAL PRIMARY KEY,
                        max_de INTEGER CHECK (max_de > 0),
                        valeur_de INTEGER CHECK (valeur_de > 0),
                        est_revele BOOLEAN,
                        est_traite BOOLEAN
                    );

                    CREATE TABLE lances_des_acteur_monstre (
                        id_de INTEGER REFERENCES de (id_de) ON DELETE CASCADE,
                        id_acteur INTEGER REFERENCES acteur (id_acteur) ON DELETE CASCADE,
                        id_monstre INTEGER REFERENCES element (id_element) ON DELETE CASCADE,
                        a_gagne VARCHAR(255),
                        CONSTRAINT lances_des_acteur_monstre_pkey PRIMARY KEY (id_acteur, id_monstre, id_de)
                    );"""
                cursor.execute(sql)
            connection.commit()
            
if __name__ == '__main__' :
    InitBDDDAO.init_bdd()