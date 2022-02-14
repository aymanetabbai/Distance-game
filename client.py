from app.client.classes_ihm.authentification.menu_authentification import MenuAuthentification

current_view = MenuAuthentification()
with open('projet-info/app/client/classes_ihm/graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
    print(asset.read())
while current_view : 
    with open('projet-info/app/client/classes_ihm/graphical_assets/border.txt', 'r', encoding="utf-8") as asset:
        print(asset.read())
    current_view.display_info()
    current_view = current_view.make_choice()
# vue closing ?