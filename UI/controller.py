import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._list_year = []
        self._list_shape = []

    def populate_dd(self):
        """ Metodo per popolare il dropdown dd_year """
        for anno in self._model.lista_anni:
            self._view.dd_year.options.append(ft.dropdown.Option(anno))

        for shape in self._model.lista_shapes:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))

        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        shape = self._view.dd_shape.value
        year = self._view.dd_year.value
        self._model.crea_grafo(shape, year)
        n1 = self._model.G.number_of_nodes()
        n2 = self._model.G.number_of_edges()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero nodi: {n1}\n'
                                                                   f'Numero di archi: {n2}'))
        for n,w in self._model.calcola_peso():
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo {n}, somma pesi su archi = {w}'))

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        percorso, peso_max = self._model.cammino_massimo()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Peso_max = {peso_max}\n'))
        for ii in percorso:
            self._view.lista_visualizzazione_2.controls.append(ft.Text(
                f'{ii[0].id} --> {ii[1].id}: weight = {ii[2]}, distance: {self._model.get_distance(ii[0], ii[1])}'))

        self._view.update()