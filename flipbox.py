import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import reportlab.lib.units as unit
import sys
import os


#パスを取得する
def get_dir_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname((sys.executable))
    else:
        base_path = os.path.dirname(__file__)
    return base_path

#pdf化
def merge_images(input_folder,output_pdf_path,text_folder,text_folder_path,spacing):
    # PDF用スペース
    pdf_path = output_pdf_path
    c = canvas.Canvas(pdf_path,  pagesize = [210 * unit.mm, 297 * unit.mm]) 
    
    # 画像をPDFに貼り付け
    size =40* unit.mm #4.1cmにリサイズ
    xpos_1 = 15*unit.mm
    xpos_2 = 15*unit.mm + size + spacing
    xpos_3 = 15*unit.mm + size*2 + spacing*2 
    xpos_4 = 15*unit.mm + size*3 + spacing*3

    # フォルダ内のすべてのファイルを取得
    files = os.listdir(input_folder)
    numberfiles = os.listdir(text_folder_path)
          
    # 画像ファイルのみを抽出
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_numberfiles = [f for f in numberfiles if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if len(image_files)<=23 or len(image_files)>=25:
        print("ごめんなさい！画像データの数は24枚ピッタリにしてほしいです！")
        messagebox.showinfo('失敗しました！','ごめんなさい！画像データの数は24枚ピッタリにしてほしいです！')
        sys.exit();
    if len(image_numberfiles)<=23 or len(numberfiles)>=25:
        print('失敗しました！',"ごめんなさい！ページ数用の画像が足りないか、多すぎるみたいです！")
        sys.exit();

    # 画像を開く
    image_count = 0
    image = []
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image.append(Image.open(image_path))
        image_count = image_count +1

    for image_numberfile in image_numberfiles:
        image_numberpath = os.path.join(text_folder_path, image_numberfile)
        image.append(Image.open(image_numberpath))

    # 画像のサイズを取得
    width, height = image[0].size

    # トリミングする範囲を計算
    top_crop = 0
    bottom_crop = height // 2

    # 画像をトリミング・合成
    cropped_image_upper = []
    cropped_image_lower = []
    merged_image = []
    
    for num in range (image_count):
        cropped_image_upper.append( image[num].crop((0, top_crop, width, height)))
        cropped_image_lower.append( image[num].crop((0, bottom_crop, width, height)))
        # 新しい画像を作成し、トリミングした画像を合成
        merged_image.append ( Image.new('RGB', (width, height), (255, 255, 255)))
        merged_image[num].paste(cropped_image_upper[num-1], (0, 0))
        merged_image[num].paste(cropped_image_lower[num], (0, height // 2))
        # 合成した画像を保存
        merged_image[num].save("out{}.png".format(num)) 
        #列の位置を指定
        line = 0
        if num > 0  and num > 3:
            line = 0
        if num > 4  and num > 7:
            line = 1
        if num > 8  and num > 11:
            line = 2
        if num > 12  and num > 15:
            line = 3
        if num > 16  and num > 19:
            line = 4
        if num > 20  and num > 23:
            line = 5
        ypos = 200*unit.mm-130*line
        #横の位置を指定
        if num % 4 ==0:
            c.drawInlineImage("out{}.png".format(num), xpos_1, ypos, size, size)
            c.drawImage("textdata/{}/{}_{}.png".format(text_folder,text_folder,num), xpos_1, ypos, size, size, preserveAspectRatio=True, mask='auto')
        if num % 4 ==1:
            c.drawInlineImage("out{}.png".format(num), xpos_2, ypos, size, size)
            c.drawImage("textdata/{}/{}_{}.png".format(text_folder,text_folder,num), xpos_2, ypos, size, size, preserveAspectRatio=True, mask='auto')
        if num % 4 ==2:
            c.drawInlineImage("out{}.png".format(num), xpos_3, ypos, size, size)
            c.drawImage("textdata/{}/{}_{}.png".format(text_folder,text_folder,num), xpos_3, ypos, size, size, preserveAspectRatio=True, mask='auto')
        if num % 4 ==3:
            c.drawInlineImage("out{}.png".format(num), xpos_4, ypos, size, size)
            c.drawImage("textdata/{}/{}_{}.png".format(text_folder,text_folder,num), xpos_4, ypos, size, size, preserveAspectRatio=True, mask='auto')
    
    #0だけやり直す 
    merged_image[0] = Image.new('RGB', (width, height), (255, 255, 255))
    merged_image[0].paste(cropped_image_upper[23], (0, 0))
    merged_image[0].paste(cropped_image_lower[0], (0, height // 2))
    merged_image[0].save("out0.png")  

    
    c.drawInlineImage("out0.png", xpos_1, 245*unit.mm, size, size)
    c.drawImage("textdata/{}/{}_0.png".format(text_folder,text_folder), xpos_1, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage("out1.png", xpos_2, 245*unit.mm, size,size)
    c.drawImage("textdata/{}/{}_1.png".format(text_folder,text_folder), xpos_2, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage("out2.png", xpos_3, 245*unit.mm, size, size)
    c.drawImage("textdata/{}/{}_2.png".format(text_folder,text_folder), xpos_3, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage("out3.png", xpos_4, 245*unit.mm, size,size)
    c.drawImage("textdata/{}/{}_3.png".format(text_folder,text_folder), xpos_4, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')

    # 合成した画像を保存
    c.save()

    #画像データを削除
    for num in range (image_count):
        os.remove("out{}.png".format(num))


#クリックされた時の処理
def on_button_click():
    # ボタンがクリックされたときの処理を追加
    # 画像のパスとPDFの出力先を指定
    dirname =  get_dir_path()
    input_folder = "{}/image".format(dirname)
    text_folder = "right_black"
    text_folder_path = "{}/textdata/{}".format(dirname,text_folder)
    output_pdf_path = "flipbox_black.pdf"
    spacing = 20  # 余白の幅

    # 画像を合成してPDFに変換
    merge_images(input_folder,output_pdf_path,text_folder,text_folder_path,spacing)

    # 画像のパスとPDFの出力先を指定
    input_folder = "{}/image".format(dirname)
    text_folder = "right_white"
    text_folder_path = "{}/textdata/{}".format(dirname,text_folder)
    output_pdf_path = "flipbox_white.pdf"
    spacing = 20  # 余白の幅

    # 画像を合成してPDFに変換
    merge_images(input_folder,output_pdf_path,text_folder,text_folder_path,spacing)
    messagebox.showinfo('PDF化成功！', 'PDF化できました！\n\n-----------------------\n\n【flipbox_black.pdf】\n【flipbox_white.pdf】\n\n-----------------------\n\nA4で印刷してね！'.format(sys.argv[0]))

# ウィンドウの作成
window = tk.Tk()
window.title("FlipboxPDFMaker")

# ラベルの作成
label = tk.Label(window, text="パラパラ漫画装置・Flipbox用のデータを作成します！")
label.pack(pady=10)

# ボタンの作成
button = tk.Button(window, text="データ作成開始！", command=on_button_click)
button.pack()

label = tk.Label(window, text="説明書は同梱の【readme.txt】をご覧ください！")
label.pack(pady=10)

# ウィンドウサイズの設定
window.geometry("400x110")  # 幅 x 高さ

# イベントループの開始
window.mainloop()