# def kol(self):
    #     self.barcode = self.bar_code.get()
    #     self.vz= self.vz_nr.get()
    #     conn = sqlite3.connect("bd.db")
    #     cursor = conn.cursor()
    #     data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand, Image_path FROM Lager_Bestand WHERE Bar_Code = ? OR VZ_Nr = ?", (self.barcode,self.vz)).fetchone()
    #     if data is not None:
    #         self.show_img_for_barcode(self.bar_code.get())
    #         self.show_img_for_vz(self.vz_nr.get())
    #         barcode_text = f"Bar Code: {data[0]}"
    #         vznr_text = f"VZ Nr: {data[1]}"
    #         bedeutung_text = f"Bedeutung: {data[2]}"
    #         Kol = f"Aktueller_bestand: {data[3]}"
    #         # Объединяем текст с значениями
    #         result_text = f"{barcode_text}\n{vznr_text}\n{bedeutung_text}\n{Kol}"
    #         self.result_show(result_text)

    #     else:
    #         self.result_show("Данного Bar Code не существует")
    #         if hasattr(self, "image_label"):
    #             self.image_label.destroy()
                
    #     cursor.close()
    #     conn.close()


