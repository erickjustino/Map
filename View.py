'''
Controller e Viewer

Authors: Erick Vinicius Justino da Silva
         Mateus Vinicius Figueredo de Araújo
'''

import tkinter as tk
from tkinter import messagebox, font
import tkintermapview as tkmv
from datetime import datetime
from PIL import Image, ImageTk


class ImageController:
    """
    Classe responsável pelo controle das imagens.
    """

    def __init__(self, bd):
        self.bd = bd

    def buscar_imagens_por_parametros(self, nome=None, data=None, cidade=None, pais=None):
        """
        Função que busca imagens no banco de dados com base nos parâmetros fornecidos.
        """
        imagens_encontradas = []

        for imagem in self.bd.todas():
            if nome and nome.lower() not in imagem.nome.lower():
                continue
            if data and data != imagem.data.date():
                continue
            if cidade and (not imagem.cidade or cidade.lower() not in imagem.cidade.lower()):
                continue
            if pais and pais.lower() != imagem.pais.lower():
                continue

            imagens_encontradas.append(imagem)

        return imagens_encontradas


class ImageViewer:
    """
    Classe responsável pela exibição das imagens.
    """

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.criando_widgets()

    def criando_widgets(self):
        """
        Função responsável pela criação dos widgets da interface gráfica.
        """
        self.root.title("Mapa de Fotos")
        self.root.configure(bg="#163172")

        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Frame de busca
        frame_search = tk.Frame(main_frame, bg="#163172")
        frame_search.pack(side=tk.LEFT, padx=10, pady=10)

        font_style = font.Font(family="8bit", size=10)

        tk.Label(frame_search, text="Nome da Imagem:", font=font_style, bg="#163172", fg="white").grid(row=0, column=0, sticky="e")
        self.entry_nome = tk.Entry(frame_search, width=60, font=font_style)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(frame_search, text="Data:", font=font_style, bg="#163172", fg="white").grid(row=1, column=0, sticky="e")
        self.entry_data = tk.Entry(frame_search, width=60, font=font_style)
        self.entry_data.grid(row=1, column=1)

        tk.Label(frame_search, text="Cidade:", font=font_style, bg="#163172", fg="white").grid(row=2, column=0, sticky="e")
        self.entry_cidade = tk.Entry(frame_search, width=60, font=font_style)
        self.entry_cidade.grid(row=2, column=1)

        tk.Label(frame_search, text="País:", font=font_style, bg="#163172", fg="white").grid(row=3, column=0, sticky="e")
        self.entry_pais = tk.Entry(frame_search, width=60, font=font_style)
        self.entry_pais.grid(row=3, column=1)

        tk.Button(frame_search, text="Buscar", command=self.procurando_images, font=font_style).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(frame_search, text="Redefinir", command=self.redefini_busca, font=font_style).grid(row=5, column=0, columnspan=2)

        # Map View
        map_frame = tk.Frame(main_frame, bg="#163172")
        map_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.map_view = tkmv.TkinterMapView(map_frame, width=600, height=600, corner_radius=0)
        self.map_view.pack(padx=5, pady=5)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_view.set_address('ECT UFRN')
        self.map_view.set_zoom(19)

        # Frame de informações da imagem
        frame_info = tk.Frame(main_frame, bg="#163172")
        frame_info.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_info, text="Nome:", font=font_style, bg="#163172", fg="white").grid(row=0, column=0, sticky="w")
        self.label_nome = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_nome.grid(row=0, column=1, sticky="w")

        tk.Label(frame_info, text="Cidade:", font=font_style, bg="#163172", fg="white").grid(row=1, column=0, sticky="w")
        self.label_cidade = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_cidade.grid(row=1, column=1, sticky="w")

        tk.Label(frame_info, text="País:", font=font_style, bg="#163172", fg="white").grid(row=2, column=0, sticky="w")
        self.label_pais = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_pais.grid(row=2, column=1, sticky="w")

        tk.Label(frame_info, text="Data:", font=font_style, bg="#163172", fg="white").grid(row=3, column=0, sticky="w")
        self.label_data = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_data.grid(row=3, column=1, sticky="w")

        tk.Label(frame_info, text="Latitude:", font=font_style, bg="#163172", fg="white").grid(row=4, column=0, sticky="w")
        self.label_latitude = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_latitude.grid(row=4, column=1, sticky="w")

        tk.Label(frame_info, text="Longitude:", font=font_style, bg="#163172", fg="white").grid(row=5, column=0, sticky="w")
        self.label_longitude = tk.Label(frame_info, width=50, anchor="w", font=font_style, bg="#163172", fg="white")
        self.label_longitude.grid(row=5, column=1, sticky="w")

    def procurando_images(self):
        """
        Função que procura imagens com base nos parâmetros fornecidos.
        """
        nome = self.entry_nome.get()
        data = self.data_pesquisa(self.entry_data.get())
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()

        imagens_encontradas = self.controller.buscar_imagens_por_parametros(nome, data, cidade, pais)

        if len(imagens_encontradas) == 0:
            messagebox.showinfo("Resultado da Busca", "Nenhuma imagem encontrada.")
        else:
            self.info_imagem(imagens_encontradas[0])
            self.mostrando_imagens_mapa(imagens_encontradas)

    def info_imagem(self, imagem):
        """
        função que exibe as informações da imagem na interface.
        """
        self.label_nome.configure(text=imagem.nome)
        self.label_cidade.configure(text=imagem.cidade)
        self.label_pais.configure(text=imagem.pais)
        self.label_data.configure(text=imagem.data.strftime("%Y-%m-%d %H:%M:%S"))
        self.label_latitude.configure(text=str(imagem.latitude))
        self.label_longitude.configure(text=str(imagem.longitude))

    def mostrando_imagens_mapa(self, imagens):
        """
        função que permite mostrar as imagens no mapa.
        """
        for imagem in imagens:
            img_anf_c = Image.open(imagem.nome)
            img_anf_c = ImageTk.PhotoImage(img_anf_c.resize(size=(204, 153)))
            self.map_view.set_marker(imagem.latitude, imagem.longitude, imagem._nome, image=img_anf_c)
            self.map_view.set_address(imagem.pais)

    def redefini_busca(self):
        """
        Função que limpa os campos de busca e reinicia a interface de dados.
        """
        self.entry_nome.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_pais.delete(0, tk.END)
        self.label_nome.configure(text="")
        self.label_cidade.configure(text="")
        self.label_pais.configure(text="")
        self.label_data.configure(text="")
        self.label_latitude.configure(text="")
        self.label_longitude.configure(text="")

    def data_pesquisa(self, date_str):
        """
        Função que converte a string de data para um objeto de data.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None


def main():
    bd = BDImagens('dataset1/index')
    bd.processa()

    root = tk.Tk()
    controller = ImageController(bd)
    image_viewer = ImageViewer(root, controller)
    root.mainloop()


if __name__ == '__main__':
    main()
