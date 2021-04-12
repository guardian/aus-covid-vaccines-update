import PyPDF2
import tabula

# urlo = '/Users/josh_nicholas/Downloads/total-number-of-people-vaccinated-for-covid-19-in-australia-4-april-2021.pdf'
urlo = '/Users/josh_nicholas/Downloads/covid-19-vaccine-rollout-update-12-april-2021_0.pdf'

# reader = PyPDF2.PdfFileReader(urlo)

# print(reader.getPage(6).extractText())

file = urlo
table = tabula.read_pdf(file,pages=7)

print(type(table[0]))

# print(table[0].columns)