from PySide2 import QtWidgets
#QtWidgets: ds ce module, il existe different fonction pour creer des interfaces graphiques
import currency_converter

class App(QtWidgets.QWidget):
      # App: herite de QtWidgets.QWidget
    def __init__(self):
        "Constructeur de la classe"
        super().__init__()
        self.c=currency_converter.CurrencyConverter() 
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.setup_css()
        self.set_default_values()
        self.setup_connexions()


    def setup_ui(self):
            """ """
        #creer un layout pour positionner les 5 widgets
            #1- creer un combobox (menu deroulant) pour afficher les devises
            #2- creer un spinbox qui va permettre de rentrer des valeurs
            #3- creer un 2eme combobox qui va etre la devise ds laquelle on veut convertir ntre montant
            #4- creer un 2eme spinbox pour afficher le montant converti
            #5- creer un push_button (bouton) pour inverser les devises
            # ts ces 5 widgets vont etre creer ds notre layout
            
            #creation des 5 widgets
            self.layout=QtWidgets.QHBoxLayout(self) # sel en parenthese pr parenter le layout a l'interface
            self.cbb_devisesFrom=QtWidgets.QComboBox() # pas besoin de sel ici, puisqu'on va le rajouter au layout
            self.spn_montant=QtWidgets.QSpinBox()

            self.cbb_devisesTo=QtWidgets.QComboBox() 
            self.spn_montantConverti=QtWidgets.QSpinBox()
            self.btn_inverser=QtWidgets.QPushButton("Inverser devises")

            #Ajout des 5 widgets
            self.layout.addWidget(self.cbb_devisesFrom)
            self.layout.addWidget(self.spn_montant)
            self.layout.addWidget(self.cbb_devisesTo)
            self.layout.addWidget(self.spn_montantConverti)
            self.layout.addWidget(self.btn_inverser)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies))) 
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies))) 
        self.cbb_devisesFrom.setCurrentText('EUR')
        self.cbb_devisesTo.setCurrentText('EUR')

        self.spn_montant.setRange(1,1000000000) #fixer l'interval acceptable
        self.spn_montantConverti.setRange(1,1000000000)

        self.spn_montant.setValue(100) # 0 à  99 par defaut ms le fait d'avoir mis a setrange avt permet d'accepter 100
        self.spn_montantConverti.setValue(100) 

    def setup_connexions(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute) 
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute(self):
        """Feature for computing"""
        montant=self.spn_montant.value()
        devise_from=self.cbb_devisesFrom.currentText()
        devise_To=self.cbb_devisesTo.currentText()

        try:
            resultat=self.c.convert(montant, devise_from,devise_To)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas reussit !!")
        else:
            self.spn_montantConverti.setValue(resultat)

    def inverser_devise(self):
        """ Inverser les devises"""

        devise_from=self.cbb_devisesFrom.currentText()
        devise_To=self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_To)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()

    def setup_css(self):
        """ stylisation et mise en forme de l'appli"""

        self.setStyleSheet("""
             background-color: rgb(30,30,30);
             color: rgb(240,240,240);   
             border:none;                       
                           """) 
             
        
        self.btn_inverser.setStyleSheet("background-color: blue;")


app=QtWidgets.QApplication([]) #  creer une appli pyside
window=App() #creer une fenetre ou widget
window.show()
app.exec_()

