import math
import tkinter as tk
from tkinter import ttk, messagebox

class RazaoLRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo da Razão L/R para Campo Magnético")
        self.root.geometry("500x400")
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header = ttk.Label(main_frame, 
                         text="CÁLCULO DA RAZÃO L/R PARA APROXIMAÇÃO DO CAMPO MAGNÉTICO",
                         style='Header.TLabel')
        header.pack(pady=(0, 10))
        
        # Frame de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(input_frame, text="Erro percentual desejado (%):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.erro_entry = ttk.Entry(input_frame)
        self.erro_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Frame de resultados
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(pady=10, fill=tk.X)
        
        # Frame para cálculo de L específico
        self.specific_frame = ttk.Frame(main_frame)
        
        ttk.Label(self.specific_frame, text="Valor de R (metros):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.r_entry = ttk.Entry(self.specific_frame)
        self.r_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        self.calc_L_button = ttk.Button(self.specific_frame, text="Calcular L", command=self.calcular_L)
        self.calc_L_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.L_result = ttk.Label(self.specific_frame, text="")
        self.L_result.grid(row=2, column=0, columnspan=2)
        
        # Botão de cálculo
        calc_button = ttk.Button(main_frame, text="Calcular Razão L/R", command=self.calcular_razao)
        calc_button.pack(pady=10)
        
        # Botão de limpar
        clear_button = ttk.Button(main_frame, text="Limpar", command=self.limpar)
        clear_button.pack(pady=5)
        
        # Configurar peso das colunas para expansão
        input_frame.columnconfigure(1, weight=1)
        self.specific_frame.columnconfigure(1, weight=1)
    
    def calcular_razao_L_sobre_R(self, erro_percentual):
        delta = erro_percentual / 100
        denominador = (1 + delta)**2 - 1
        return math.sqrt(4 / denominador)
    
    def calcular_razao(self):
        try:
            # Limpar resultados anteriores
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            
            erro = float(self.erro_entry.get())
            if erro <= 0:
                messagebox.showerror("Erro", "O erro deve ser positivo.")
                return
                
            razao = self.calcular_razao_L_sobre_R(erro)
            
            # Exibir resultados
            ttk.Label(self.result_frame, 
                     text=f"Para um erro de {erro}%:").pack(anchor=tk.W)
            ttk.Label(self.result_frame, 
                     text=f"A razão L/R deve ser ≈ {razao:.4f}").pack(anchor=tk.W)
            ttk.Label(self.result_frame, 
                     text=f"Ou seja: L ≈ {razao:.4f} × R").pack(anchor=tk.W)
            
            # Mostrar frame para cálculo específico
            self.specific_frame.pack(pady=10, fill=tk.X)
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido para o erro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    
    def calcular_L(self):
        try:
            razao_text = self.result_frame.winfo_children()[1].cget("text")
            razao = float(razao_text.split("≈ ")[1])
            
            R = float(self.r_entry.get())
            if R <= 0:
                messagebox.showerror("Erro", "O valor de R deve ser positivo.")
                return
                
            L = razao * R
            self.L_result.config(text=f"Para R = {R} m, o comprimento mínimo é L ≈ {L:.4f} m")
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido para R.")
        except IndexError:
            messagebox.showerror("Erro", "Calcule primeiro a razão L/R.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    
    def limpar(self):
        self.erro_entry.delete(0, tk.END)
        self.r_entry.delete(0, tk.END)
        
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        self.L_result.config(text="")
        self.specific_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = RazaoLRApp(root)
    root.mainloop()