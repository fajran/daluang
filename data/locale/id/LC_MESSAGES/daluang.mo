��          �   %   �      P     Q     h  	   x  %   �  E   �  D   �  \   3  *   �     �     �  3   �       /         P  0   ^  1   �     �    �  R  N  �   �  �   v    t	     �
     �
     �
  6  �
     �       	     '      L   H  E   �  f   �  1   B     t     �  3   �     �  2   �       4      9   U     �  �  �  �  3  �   �  	  �  W  �     	       	   -               	             
                                                                                                 Available commands: %s Available data: Category: Click here to open the online version Daluang could not found anything about <strong>%(keywords)s</strong>. Daluang doesn't have an article called <strong>%(article)s</strong>. Daluang doesn't have data for <strong>%(article)s</strong> in <strong>%(language)s</strong>. Need help?
	
Usage: daluang help <command> No data available Not found: %s Open online version of <strong>%(article)s</strong> Other languages: Search content for <strong>%(article)s</strong> Search result Search result for <strong>%(keywords)s</strong>: Search wikipedia for <strong>%(article)s</strong> Suggestions: This command is used to convert a data from Wikipedia's format to Daluang own format.
	
Usage: daluang convert <language> <code> <data>

    <data> is an XML database dump of Wikipedia. Usually it is written in the following format:

        idwiki-20080213-pages-articles.xml.bz2
	
Example usage:

    $ daluang convert "Bahasa Indonesia" "id" idwiki-20080213-pages-articles.xml.bz2 This command is used to create a Xapian index of a data.
	
Usage: daluang index <data> <database>

    <data> is a Daluang's data and <database> is a target Xapian's database.

You have to install python-xapian package in order to use this function. This operation may take very long time!
	
Example usage:

    $ daluang index id.data id This command is used to list installed data.

Each line will be written in the following format:

    [code] langauge

Example:

    [id] Bahasa Indonesia

The value of "code" is used when you use "read" command. This command is used to read an article from Daluang data.
	
Usage: daluang read <datafile|code> <title>

    <datafile|code> is either a data file or a language code.

Example usage:

    $ daluang read id.data "bandung"
    $ daluang read id "bandung" Usage: daluang <command> [cmd-opt ...]

Available commands:

- convert : convertes a wikipedia dump file
- index   : creates Xapian's index for a daluang data
- list    : lists all installed wikipedia files
- read    : reads a wikipedia entry
- help    : help for other commands hide python-xapian doesn't exist show Project-Id-Version: 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2008-04-05 20:36+0200
PO-Revision-Date: 2008-04-05 15:28+0200
Last-Translator: Fajran Iman Rusadi <fajran@gmail.com>
Language-Team: Indonesian Translator
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 Perintah yang tersedia: %s Data yang tesedia: Kategori: Klik di sini untuk membuka versi online Daluang tidak dapat menemukan apapun mengenai <strong>%(keywords)s</strong>. Daluang tidak memiliki artikel berjudul <strong>%(article)s</strong>. Daluang tidak memiliki data mengenai <strong>%(article)s</strong> dalam <strong>%(language)s</strong>. Butuh bantuan?
	
Gunakan: daluang help <perintah> Data tidak tersedia Tidak ditemukan: %s Buka versi online dari <strong>%(article)s</strong> Bahasa lain: Cari artikel mengenai <strong>%(article)s</strong> Hasil pencarian Hasil pencarian untuk <strong>%(keywords)s</strong>: Cari pada wikipedia mengenai <strong>%(article)s</strong> Saran: Perintah ini digunakan untuk mengkonversi data dari format Wikipedia menjadi format data milik Daluang.
	
Gunakan: daluang convert <bahasa> <kode> <data>

    <data> adalah berkas basisdata Wikipedia dalam bentuk XML. Biasanya tertulis dalam format berikut:

        idwiki-20080213-pages-articles.xml.bz2
	
Contoh penggunaan:

    $ daluang convert "Bahasa Indonesia" "id" idwiki-20080213-pages-articles.xml.bz2 Perintah ini digunakan untuk membuat berkas indeks Xapian dari data yang ada.
	
Gunakan: daluang index <data> <basisdata>

    <data> adalah data dalam Daluang dan <basisdata> adalah basis data Xapianyang dituju.

Anda harus memasang paket python-xapian jika ingin menggunakan fungsi ini. Operasi ini mungkin membutuhkan waktu yang sangat lama!
	
Contoh penggunaan:

    $ daluang index id.data id Perintah ini digunakan untuk melihat data yang terpasang.

Setiap baris akan ditulis dalam format berikut:

    [kode] bahasa

Contoh:

    [id] Bahasa Indonesia

Nilai dari "kode" digunakan saat anda menggunakan perintah "read". Perintah ini digunakan untuk membaca sebuah artikel dari Daluang.
	
Gunakan: daluang read <berkasdata|kode> <judul>

    <berkasdata|kode> adalah berkas data atau kode bahasa.

Contoh penggunaan:

    $ daluang read id.data "bandung"
    $ daluang read id "bandung" Gunakan: daluang <perintah> [cmd-opt ...]

Perintah yang tersedia:

- convert : mengkonversi berkas wikipedia dump
- index   : membuat berkas indeks bagi Xapian dari data Daluang
- list    : menampilkan seluruh berkas data Wikipedia yang terpasang
- read    : membaca sebuah tulisan di Wikipedia
- help    : membaca bantuan untuk perintah lain sembunyikan python-xapian tidak ada tampilkan 