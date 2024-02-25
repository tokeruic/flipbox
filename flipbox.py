
#####################################################################################
#
#	Copyright (c) 2000-2014, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################


import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import reportlab.lib.units as unit
import sys
import webbrowser


#パスを取得する
def get_dir_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.join(os.path.dirname((sys.executable)))
    else:
        base_path = os.path.join(os.path.dirname(__file__))
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

    #チェックボックス情報取得
    frame = frame_var.get()
    lineflag = center_line_var.get()

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
        merged_image[num].save(os.path.join(os.path.dirname(__file__), "out{}.png".format(num))) 
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
            c.drawInlineImage(os.path.join(os.path.dirname(__file__), "out{}.png".format(num)), xpos_1, ypos, size, size)
            c.drawImage(os.path.join(os.path.dirname(__file__), "textdata/{}/{}_{}.png".format(text_folder,text_folder,num)), xpos_1, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if frame == True:
                c.drawImage(os.path.join(os.path.dirname(__file__), "frame.png".format(text_folder,text_folder,num)), xpos_1, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if lineflag == True:
                c.drawImage(os.path.join(os.path.dirname(__file__), "line.png".format(text_folder,text_folder,num)), xpos_1, ypos, size, size, preserveAspectRatio=True, mask='auto') 
        if num % 4 ==1:
            c.drawInlineImage(os.path.join(os.path.dirname(__file__), "out{}.png".format(num)), xpos_2, ypos, size, size)
            c.drawImage(os.path.join(os.path.dirname(__file__), "textdata/{}/{}_{}.png".format(text_folder,text_folder,num)), xpos_2, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if frame == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_2, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if lineflag == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_2, ypos, size, size, preserveAspectRatio=True, mask='auto')
        if num % 4 ==2:
            c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out{}.png".format(num)), xpos_3, ypos, size, size)
            c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_{}.png".format(text_folder,text_folder,num)), xpos_3, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if frame == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_3, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if lineflag == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_3, ypos, size, size, preserveAspectRatio=True, mask='auto')
        if num % 4 ==3:
            c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out{}.png".format(num)), xpos_4, ypos, size, size)
            c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_{}.png".format(text_folder,text_folder,num)), xpos_4, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if frame == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_4, ypos, size, size, preserveAspectRatio=True, mask='auto')
            if lineflag == True:
                c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_4, ypos, size, size, preserveAspectRatio=True, mask='auto')

   
    #0だけやり直す 
    merged_image[0] = Image.new('RGB', (width, height), (255, 255, 255))
    merged_image[0].paste(cropped_image_upper[23], (0, 0))
    merged_image[0].paste(cropped_image_lower[0], (0, height // 2))
    merged_image[0].save(os.path.join(os.path.dirname(__file__),"out0.png"))  

    
    c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out0.png"), xpos_1, 245*unit.mm, size, size)
    c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_0.png".format(text_folder,text_folder)), xpos_1, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if frame == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_1, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if lineflag == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_1, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out1.png"), xpos_2, 245*unit.mm, size,size)
    c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_1.png".format(text_folder,text_folder)), xpos_2, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if frame == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_2, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if lineflag == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_2, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out2.png"), xpos_3, 245*unit.mm, size, size)
    c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_2.png".format(text_folder,text_folder)), xpos_3, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if frame == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_3, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if lineflag == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_3, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    c.drawInlineImage(os.path.join(os.path.dirname(__file__),"out3.png"), xpos_4, 245*unit.mm, size,size)
    c.drawImage(os.path.join(os.path.dirname(__file__),"textdata/{}/{}_3.png".format(text_folder,text_folder)), xpos_4, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if frame == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"frame.png"), xpos_4, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
    if lineflag == True:
        c.drawImage(os.path.join(os.path.dirname(__file__),"line.png"), xpos_4, 245*unit.mm, size, size, preserveAspectRatio=True, mask='auto')
 
    # 合成した画像を保存
    c.save()

    #画像データを削除
    for num in range (image_count):
        os.remove(os.path.join(os.path.dirname(__file__),"out{}.png".format(num)))


#生成ボタンがクリックされた時の処理
def on_button_click():
    # ボタンがクリックされたときの処理を追加
    # 画像のパスとPDFの出力先を指定
    dirname =  get_dir_path()
    input_folder = "{}/image".format(dirname)
    input_folder = os.path.join(os.path.dirname(__file__), input_folder)
    text_folder = "right_black"
    text_folder_path = "{}/textdata/{}".format(dirname,text_folder)
    text_folder_path = os.path.join(os.path.dirname(__file__), "{}/textdata/{}".format(dirname,text_folder))
    output_pdf_path = "flipbox_black.pdf"
    spacing = 20  # 余白の幅

    # 画像を合成してPDFに変換
    merge_images(input_folder,output_pdf_path,text_folder,text_folder_path,spacing)

    # 画像のパスとPDFの出力先を指定
    input_folder = os.path.join(os.path.dirname(__file__), "{}/image".format(dirname))
    text_folder = "right_white"
    text_folder_path = os.path.join(os.path.dirname(__file__), "{}/textdata/{}".format(dirname,text_folder))
    output_pdf_path = "flipbox_white.pdf"
    spacing = 20  # 余白の幅

    # 画像を合成してPDFに変換
    merge_images(input_folder,output_pdf_path,text_folder,text_folder_path,spacing)
    messagebox.showinfo('PDF化成功！', 'PDF化できました！\n\n-----------------------\n\n【flipbox_black.pdf】\n【flipbox_white.pdf】\n\n-----------------------\n\nA4で印刷してね！'.format(sys.argv[0]))

#フレームをつけるボタンがオンの時の処理
def toggle_frame_button():
    if frame_var.get() == 1:  # チェックボックスがオンの場合
        color_button_frame.grid(row=3, column=2,sticky=tk.W,padx=5, pady=5)  # 色選択ボタンを表示
    else:
        color_button_frame.grid_forget()  # 色選択ボタンを非表示

#中央に線をつけるボタンがオンの時の処理
def toggle_line_button():
    if center_line_var.get() == 1:  # チェックボックスがオンの場合
        color_button_line.grid(row=2, column=2,sticky=tk.W,padx=5, pady=5)  # 色選択ボタンを表示
    else:
        color_button_line.grid_forget()  # 色選択ボタンを非表示

#色を選ぶ処理
def choose_color_frame():
    color = colorchooser.askcolor(title="色を選択してください")
    if color[1]:  # 色が選択された場合
        print("選択された色:", color[1])
    if frame_var.get() == 1: 
        #フレーム画像生成
        # 画像のサイズ
        width, height = 720, 720
        # 新しい画像を作成します
        frame_image = Image.new("RGB", (width, height), color[1])
        # マスク用の画像を生成
        mask = Image.open('textdata/frame_mask.png').convert('1').resize(frame_image.size)
        frame_image.putalpha(mask)
        frame_image.save("frame.png")
            

#色を選ぶ処理
def choose_color_line():
    color = colorchooser.askcolor(title="色を選択してください")
    if color[1]:  # 色が選択された場合
        print("選択された色:", color[1])
    if center_line_var.get() == 1: 
        #フレーム画像生成
        # 画像のサイズ
        width, height = 720, 720
        # 新しい画像を作成します
        line_image = Image.new("RGB", (width, height), color[1])
        # マスク用の画像を生成
        mask = Image.open('textdata/center_mask.png').convert('1').resize(line_image.size)
        line_image.putalpha(mask)
        line_image.save("line.png")


#説明書の処理
def help():
    url = "https://github.com/tokeruic/flipbox"
    webbrowser.open(url, new=0, autoraise=True)

# ウィンドウの作成
window = tk.Tk()
window.title("FlipboxPDFMaker")

# ラベルの作成
label = tk.Label(window, text="Flipbox用のPDFデータを制作します！")
label.grid(row = 0, column = 0, sticky = tk.W, padx = 5, pady = 5) 

# チェックボックスの作成
center_line_var= tk.BooleanVar() 
chk = tk.Checkbutton(text='中央に線をつける',variable = center_line_var, command=toggle_line_button)
chk.grid(row = 2, column = 0, columnspan = 2, sticky = tk.W, padx = 5, pady = 5)  

# チェックボックスの作成
frame_var = tk.IntVar()
check_button = tk.Checkbutton(window, text="フレームをつける", variable=frame_var, command=toggle_frame_button)
check_button.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W, padx = 5, pady = 5) 

# 色選択ボタンの作成
color_button_frame = tk.Button(window, text="フレームの色を選択", command=choose_color_frame)

# 色選択ボタンの作成
color_button_line = tk.Button(window, text="中央の線の色を選択", command=choose_color_line)



# ボタンの作成
button = tk.Button(window, text="データ作成開始！", command=on_button_click)
button.grid(row = 8, column = 0, columnspan = 2, sticky = tk.EW, padx = 5, pady = 5)  


# menubarの作成
menubar = tk.Menu(window)
window.config(menu=menubar)


# menubarにヘルプメニューを作成
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='ヘルプ', menu=help_menu)
# ヘルプメニューにプルダウンメニューを追加
help_menu.add_command(label='説明書',command = help)

# ウィンドウサイズの設定
window.geometry("320x150")  # 幅 x 高さ

# イベントループの開始
window.mainloop()