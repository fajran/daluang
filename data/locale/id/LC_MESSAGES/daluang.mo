��    5      �  G   l      �  	   �     �     �     �     �     �     �  	   �  %   �          .     E  :   X  :   �  H   �          0     6     >     Q  /   j     �     �  	   �     �     �     �     �  *   �  #   %     I     Z     t  &   {     �  %   �  (   �     �  ,        ;  �  H  \  �	  �   /             -  Q   1     �     �     �     �     �  C  �               !     /     C     ^     r  	   y  '   �     �     �     �  B   �  <   ,  S   i     �     �     �     �  "   �  6   !     X     ^     r     �     �     �     �  *   �  "   �          &     B  )   G     q  *   �  0   �     �  1   �       �  $  �  �  �   Z    @  \  T     �  a   �          "     >  	   V     `        %         #   0   1                   )      ,           (      /         *              .                     3              -   $   
             2   	      '                 5          "       &                           !             4      +    All Pages Always Article title Available Languages Available commands: %s Available data: Back Category: Click here to open the online version Content not available Content not available! Content not found! Daluang could not found anything about <strong>%s</strong> Daluang doesn't have an article called <strong>%s</strong> Daluang doesn't have data for <strong>%s</strong> in <strong>%s</strong> Do you want to continue? Extra Forward Language list page List all available pages Need help?
	
Usage: daluang-util help <command> No No data available Not found Not found: %s Open Wikipedia Open article Open external browser? Open online version of <strong>%s</strong> Open online version of this article Other languages: Please install some data. Search Search content for <strong>%s</strong> Search result Search result for <strong>%s</strong> Search wikipedia for <strong>%s</strong> Show all pages Starting Daluang server at %(addr)s:%(port)s Suggestions: This command is used to convert a data from Wikipedia's format to Daluang own format.
	
Usage: daluang-util convert <language> <code> <data>

    <data> is an XML database dump of Wikipedia. Usually it is written in the following format:

        idwiki-20080213-pages-articles.xml.bz2
	
Example usage:

    $ daluang-util convert "Bahasa Indonesia" "id" idwiki-20080213-pages-articles.xml.bz2 This command is used to create a Xapian index of a data.
	
Usage: daluang-util index <data> <database>

    <data> is a Daluang's data and <database> is a target Xapian's database.

You have to install python-xapian package in order to use this function. This operation may take very long time!
	
Example usage:

    $ daluang-util index id.data id This command is used to list installed data.

Each line will be written in the following format:

    [code] langauge

Example:

    [id] Bahasa Indonesia

The value of "code" is used when you use "read" command. This command is used to read an article from Daluang data.
	
Usage: daluang-util read <datafile|code> <title>

    <datafile|code> is either a data file or a language code.

Example usage:

    $ daluang-util read id.data "bandung"
    $ daluang-util read id "bandung" Usage: daluang-util <command> [cmd-opt ...]

Available commands:

- convert : convertes a wikipedia dump file
- index   : creates Xapian's index for a daluang data
- list    : lists all installed wikipedia files
- read    : reads a wikipedia entry
- help    : help for other commands Yes You clicked an external link and Daluang is going to open it on external browser. hide http://example.com/article/ python-xapian doesn't exist show to Project-Id-Version: 0.1
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2008-10-07 12:27+0200
PO-Revision-Date: 2008-04-05 15:28+0200
Last-Translator: Fajran Iman Rusadi <fajran@gmail.com>
Language-Team: Indonesian Translator
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 Semua Halaman Selalu Judul artikel Bahasa Yang Tesedia Perintah yang tersedia: %s Data yang tersedia: Mundur Kategori: Klik di sini untuk membuka versi online Data tidak tersedia Data tidak tersedia! Data tidak tersedia! Daluang tidak dapat menemukan apapun mengenai <strong>%s</strong>. Daluang tidak memiliki artikel berjudul <strong>%s</strong>. Daluang tidak memiliki data mengenai <strong>%s</strong> dalam <strong>%s</strong>. Apakah Anda ingin melanjutkan? Ekstra Maju Halaman daftar bahasa Tampilkan seluruh halaman yang ada Butuh bantuan?
	
Gunakan: daluang-util help <perintah> Tidak Data tidak tersedia Tidak ditemukan Tidak ditemukan: %s Buka Wikipedia Buka artikel Buka peramban eksternal? Buka versi online dari <strong>%s</strong> Buka versi online dari artikel ini Bahasa lain: Harap pasang beberapa data. Cari Cari artikel mengenai <strong>%s</strong> Hasil pencarian Hasil pencarian untuk <strong>%s</strong>: Cari pada wikipedia mengenai <strong>%s</strong> Semua halaman Menjalankan server Daluang pada %(addr)s:%(port)s Saran: Perintah ini digunakan untuk mengkonversi data dari format Wikipedia menjadi format data milik Daluang.
	
Gunakan: daluang-util convert <bahasa> <kode> <data>

    <data> adalah berkas basisdata Wikipedia dalam bentuk XML. Biasanya tertulis dalam format berikut:

        idwiki-20080213-pages-articles.xml.bz2
	
Contoh penggunaan:

    $ daluang convert "Bahasa Indonesia" "id" idwiki-20080213-pages-articles.xml.bz2 Perintah ini digunakan untuk membuat berkas indeks Xapian dari data yang ada.
	
Gunakan: daluang-util index <data> <basisdata>

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

    $ daluang-util read id.data "bandung"
    $ daluang-util read id "bandung" Gunakan: daluang-util <perintah> [cmd-opt ...]

Perintah yang tersedia:

- convert : mengkonversi berkas wikipedia dump
- index   : membuat berkas indeks bagi Xapian dari data Daluang
- list    : menampilkan seluruh berkas data Wikipedia yang terpasang
- read    : membaca sebuah tulisan di Wikipedia
- help    : membaca bantuan untuk perintah lain Ya Anda mengklik sebuah tautan eksternal dan Daluang akan membuka peramban internetuntuk membukanya. sembunyikan http://example.com/article/ python-xapian tidak ada tampilkan sampai 