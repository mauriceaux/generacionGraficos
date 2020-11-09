import os

def generarTex(file,graficoConvergencia,instancia,escaleColumnWidth,formatoGraficos):
    file.write("\\begin{figure}[H]")
    file.write("\\begin{center}")
    
    if formatoGraficos == "png":
        file.write(f'	\\includegraphics[width={escaleColumnWidth}\\columnwidth]{{{graficoConvergencia}\\gc-{graficoConvergencia}-{instancia}.png}}')
    elif formatoGraficos == "eps":
        file.write(f'	\\includegraphics[width={escaleColumnWidth}\\columnwidth]{{{graficoConvergencia}\\gc-{graficoConvergencia}-{instancia}.eps}}')

    file.write(f'	\\caption{{{graficoConvergencia}}}')
    file.write(f'\\label{{{graficoConvergencia}}}')
    file.write("\\end{center}")
    file.write("\\end{figure}")
    file.write(os.linesep)
