��    .      �  =   �      �     �     �               1     A  	   F  %   P     v     �  E   �  D   �  \   .     �     �     �  *   �     �     �  	   �     	          $     ;  3   O     �     �     �  /   �     �  0   �  1   $  ,   V     �    �  R  	  �   c
  �   8    6     M  Q   Q     �     �     �     �  6  �          #     1     F     a     u  	   |  '   �     �     �  L   �  E   $  f   j     �     �     �  1        =     C     W     g     {     �     �  3   �     �     �       2        H  4   X  9   �  1   �     �  �     �  �  �   ,  	    W       t  a   w     �     �       	        ,       !   %                           
   (   &                            +      )                -                        *      #      $              	                             "         '      .          Always Article title Available Languages Available commands: %s Available data: Back Category: Click here to open the online version Content not available Content not available! Daluang could not found anything about <strong>%(keywords)s</strong>. Daluang doesn't have an article called <strong>%(article)s</strong>. Daluang doesn't have data for <strong>%(article)s</strong> in <strong>%(language)s</strong>. Do you want to continue? Forward Language list page Need help?
	
Usage: daluang help <command> No No data available Not found Not found: %s Open article Open external browser? Open online version Open online version of <strong>%(article)s</strong> Other languages: Please install some data. Search Search content for <strong>%(article)s</strong> Search result Search result for <strong>%(keywords)s</strong>: Search wikipedia for <strong>%(article)s</strong> Starting Daluang server at %(addr)s:%(port)s Suggestions: This command is used to convert a data from Wikipedia's format to Daluang own format.
	
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
- help    : help for other commands Yes You clicked an external link and Daluang is going to open it on external browser. hide http://example.com/article/ python-xapian doesn't exist show Project-Id-Version: 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2008-04-25 21:11+0200
PO-Revision-Date: 2008-04-05 15:28+0200
Last-Translator: Fajran Iman Rusadi <fajran@gmail.com>
Language-Team: Indonesian Translator
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 Selalu Judul artikel Bahasa Yang Tesedia: Perintah yang tersedia: %s Data yang tersedia: Mundur Kategori: Klik di sini untuk membuka versi online Data tidak tersedia Data tidak tersedia! Daluang tidak dapat menemukan apapun mengenai <strong>%(keywords)s</strong>. Daluang tidak memiliki artikel berjudul <strong>%(article)s</strong>. Daluang tidak memiliki data mengenai <strong>%(article)s</strong> dalam <strong>%(language)s</strong>. Apakah Anda ingin melanjutkan? Maju Halaman daftar bahasa Butuh bantuan?
	
Gunakan: daluang help <perintah> Tidak Data tidak tersedia Tidak ditemukan Tidak ditemukan: %s Buka artikel Buka peramban eksternal? Buka versi online Buka versi online dari <strong>%(article)s</strong> Bahasa lain: Harap pasang beberapa data. Cari Cari artikel mengenai <strong>%(article)s</strong> Hasil pencarian Hasil pencarian untuk <strong>%(keywords)s</strong>: Cari pada wikipedia mengenai <strong>%(article)s</strong> Menjalankan server Daluang pada %(addr)s:%(port)s Saran: Perintah ini digunakan untuk mengkonversi data dari format Wikipedia menjadi format data milik Daluang.
	
Gunakan: daluang convert <bahasa> <kode> <data>

    <data> adalah berkas basisdata Wikipedia dalam bentuk XML. Biasanya tertulis dalam format berikut:

        idwiki-20080213-pages-articles.xml.bz2
	
Contoh penggunaan:

    $ daluang convert "Bahasa Indonesia" "id" idwiki-20080213-pages-articles.xml.bz2 Perintah ini digunakan untuk membuat berkas indeks Xapian dari data yang ada.
	
Gunakan: daluang index <data> <basisdata>

    <data> adalah data dalam Daluang dan <basisdata> adalah basis data Xapian yang dituju.

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
- help    : membaca bantuan untuk perintah lain Ya Anda mengklik sebuah tautan eksternal dan Daluang akan membuka peramban internetuntuk membukanya. sembunyikan http://example.com/article/ python-xapian tidak ada tampilkan 