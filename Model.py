'''
Módulo imagem.

Contém classes para manipular
imagens georreferenciadas (com informação de GPS)

Authors: Erick Vinicius Justino da Silva
         Mateus Vinicius Figueredo de Araújo
'''

from datetime import datetime
from PIL import Image
import PIL.ImageFile
from PIL.ExifTags import TAGS, GPSTAGS
from typing import List, Tuple
import tkintermapview as tkmv

def converte_graus_para_decimais(tup: Tuple[int, int, int], ref: str) -> float:
    '''
    Função utilitária: converte coordenadas de
    graus, minutos e segundos (tupla) para
    decimais (float).
    '''
    if ref.upper() in ('N', 'E'):
        s = 1
    elif ref.upper() in ('S', 'W'):
        s = -1

    return s*(tup[0] + float(tup[1]/60) + float(tup[2]/3600))

class Imagem:
    '''
    Representa uma imagem
    (classe principal do programa).
    '''

    def __init__(self, nome):
        '''
        Inicializa um objeto imagem
        a partir do nome do seu arquivo.
        '''
        self._img = self.abre(nome) # abre imagem a partir do seu nome
        self._nome = nome.rsplit('/')[-1] # nome do arquivo da imagem
        self._data = None # data de captura da imagem
        self._lat = None # latitude da captura da imagem
        self._lon = None # longitude da captura da imagem
        self._cidade = None  # cidade da captura da imagem
        self._pais = None  # país da captura da imagem
        self._processa_EXIF()

    def __repr__(self) -> str:
        '''
        Retorna representação de uma imagem
        em forma de str.
        '''
        return self._nome

    def _processa_EXIF(self) -> None:
        '''
        Processa metadados EXIF contidos no arquivo da imagem
        para extrair informações de data, localização (latitude, longitude, cidade e país) de captura.

        Atribui valores aos atributos de instância correspondentes
        à latitude, longitude, cidade, país e data de captura.
        '''
        tup_lat = None
        tup_lon = None
        ref_lat = None
        ref_lon = None

        for c, v in self._img._getexif().items():
            if TAGS[c] == 'GPSInfo':
                for gps_cod, gps_dado in v.items():
                    if GPSTAGS[gps_cod] == 'GPSLatitude':
                        tup_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitude':
                        tup_lon = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLatitudeRef':
                        ref_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitudeRef':
                        ref_lon = gps_dado

                self._lat = converte_graus_para_decimais(tup_lat, ref_lat)
                self._lon = converte_graus_para_decimais(tup_lon, ref_lon)

            if TAGS[c] == 'DateTime':
                self._data = datetime.strptime(v, '%Y:%m:%d %H:%M:%S')

        self._cidade = tkmv.convert_coordinates_to_city(self.latitude, self.longitude)
        self._pais = tkmv.convert_coordinates_to_country(self.latitude, self.longitude)

    @staticmethod
    def abre(nome: str) -> PIL.ImageFile:
        '''
        Abre imagem a partir de
        arquivo com o nome
        fornecido.
        Retorna objeto imagem
        aberto.
      '''
        img = Image.open(nome)
        return img

    @property
    def nome(self) -> str:
        '''
        Retorna o nome do arquivo
        da imagem.
        '''
        return self._nome

    @property
    def largura(self) -> int:
        '''
        Retorna a largura da imagem.
        '''
        return self._img.width

    @property
    def altura(self) -> int:
        '''
        Retorna a altura da imagem.
        '''
        return self._img.height

    @property
    def tamanho(self) -> Tuple[int, int]:
        '''
        Retorna o tamanho da imagem
        (tupla largura x altura).
        '''
        return self._img.size

    @property
    def data(self) -> datetime:
        '''
        Retorna a data em que a imagem
        foi capturada (objeto da classe datetime).
        '''
        return self._data

    @property
    def latitude(self) -> float:
        '''
        Retorna a latitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lat

    @property
    def longitude(self) -> float:
        '''
        Retorna a longitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lon

    @property
    def cidade(self) -> str:
        '''
        Retorna a cidade em que a imagem foi capturada.
        '''
        return self._cidade

    @property
    def pais(self) -> str:
        '''
        Retorna o país em que a imagem foi capturada.
        '''
        return self._pais

    def imprime_info(self) -> None:
        '''
        Imprime informações sobre
        a imagem.
        '''
        print(f'Largura: {self._img.width}')
        print(f'Altura: {self._img.height}')
        print(f'L x A: {self._img.size}')
        print(f'Nome: {self._nome}')
        print(f'Latitude: {self._lat}')
        print(f'Longitude: {self._lon}')
        print(f'Cidade: {self._cidade}')
        print(f'País: {self._pais}')
        print(f'Data:{self._data}')

    def redimensiona(self, nv_lar: float, nv_alt: float) -> None:
        '''
        Altera as dimensões do objeto imagem para
        que ele possua novo tamanho dado por
        nv_lar x nv_alt.
        '''
        img_redimensionada = self._img.resize((int(nv_lar), int(nv_alt)))
        self._img = img_redimensionada


class BDImagens:
    '''
    Representa um banco de dados de
    imagens geoespaciais
    (classe de busca do programa).
    '''

    def __init__(self, idx):
        self._idx = idx  # Caminho para o arquivo de índice
        self._imagens = []  # Lista para armazenar as imagens

    def processa(self) -> None:
        '''
        Abre cada imagem no arquivo de índice
        e adiciona cada imagem à lista.
        '''
        with open(self._idx) as arq:
            for linha in arq:
                nome_img = linha.strip()
                imagem = Imagem(nome_img)
                self._imagens.append(imagem)

    @property
    def tamanho(self) -> int:
        '''
        Retorna a quantidade de imagem
        no banco de dados.
        '''
        return len(self._imagens)

    def todas(self) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens abertas
        no banco de dados.
        '''
        return self._imagens

    def busca_por_nome(self, texto: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados cujo nome contenha o texto passado como parâmetro.
        '''
        imgs_encontradas_nome = []
        for imagem in self._imagens:
            if texto in imagem.nome:
                imgs_encontradas_nome.append(imagem)
        return imgs_encontradas_nome

    def busca_por_data(self, dini: datetime, dfim: datetime) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja data de captura encontra-se entre
        dini (data inicial) e dfim (data final).
        '''
        imgs_encontradas_data = []
        for imagem in self._imagens:
            if dini <= imagem.data <= dfim:
                imgs_encontradas_data.append(imagem)
        return imgs_encontradas_data

    def busca_por_cidade(self, cidade: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados cuja cidade de captura corresponda à cidade fornecida.
        '''
        imgs_encontradas_cidade = []
        for imagem in self._imagens:
            if imagem.cidade == cidade:
                imgs_encontradas_cidade.append(imagem)
        return imgs_encontradas_cidade

    def busca_por_pais(self, pais: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados cujo país de captura corresponda ao país fornecido.
        '''
        imgs_encontradas_pais = []
        for imagem in self._imagens:
            if imagem.pais == pais:
                imgs_encontradas_pais.append(imagem)
        return imgs_encontradas_pais

def main():

    bd = BDImagens('dataset1/index')
    bd.processa()   

    # Mostra as informações de todas as imagens do banco de dados
    print('Imagens do Banco de Dados:')
    for img in bd.todas():
        img.imprime_info()

    # Mostra os nomes das imagens que possuam texto no seu nome
    texto = '06'
    print(f'Imagens com "{texto}" no nome:')
    for img in bd.busca_por_nome(texto):
        print(img.nome)

    # Mostra as datas das imagens capturadas entre d1 e d2
    d1 = datetime(2021, 1, 1)
    d2 = datetime(2023, 1, 1)
    print(f'Imagens capturadas entre {d1} e {d2}:')
    for img in bd.busca_por_data(d1, d2):
        print(img.data)

    # Mostra as imagens capturadas em uma cidade específica
    cidade = 'Natal'
    print(f'Imagens capturadas em {cidade}:')
    for img in bd.busca_por_cidade(cidade):
        print(img.nome)

    # Mostra as imagens capturadas em um país específico
    pais = 'Brasil'
    print(f'Imagens capturadas no {pais}:')
    for img in bd.busca_por_pais(pais):
        print(img.nome)

if __name__ == '__main__':
    main()