from Model import BDImagens
from View import Mapa

class MapaController:
    def __init__(self):
        self.bd = BDImagens('dataset1/index')
        self.bd.processa()
        self.mapa = Mapa()
        self.mapa.imagens = self.bd.todas()

        # Conectar os eventos da view aos métodos do controller
        self.mapa.buscar_imagens_evento = self.buscar_imagens
        self.mapa.redefinir_busca_evento = self.redefinir_busca

    def buscar_imagens(self, nome, cidade, pais, data_inicial, data_final):
        # Filtro das imagens
        self.resultados = [imagem for imagem in self.imagens if
                   (nome == "" or imagem.nome.lower() == nome.lower()) and
                   (cidade == "" or imagem.cidade.lower() == cidade.lower()) and
                   (pais == "" or imagem.pais.lower() == pais.lower()) and
                   (data_inicial == "" or imagem.data_inicial >= data_inicial) and
                   (data_final == "" or imagem.data_final <= data_final)]


        if len(self.mapa.resultados) == 0:
            self.mapa.mostrar_mensagem("Sem Resultados", "Nenhum resultado encontrado.")
        else:
            self.mapa.exibir_resultados()

    def redefinir_busca(self):
        self.mapa.resultados = self.mapa.imagens
        self.mapa.limpar_campos_busca()
        self.mapa.exibir_resultados()

    def run(self):
        self.mapa.executa()


def main():
    controller = MapaController()
    controller.run()


if __name__ == '__main__':
    main()