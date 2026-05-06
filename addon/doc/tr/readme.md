# IBMTTS sürücüsü, NVDA için eklenti

Bu eklenti, NVDA ile IBMTTS sentezleyicisi arasında uyumluluk sağlar.
IBMTTS kütüphanelerini dağıtamıyoruz. Bu nedenle bu sadece sürücüdür.
Bu sürücüyü geliştirmek isterseniz, Çekme isteklerinizi göndermekten çekinmeyin!

Bu sürücü Eloquence kütüphaneleriyle uyumludur (çünkü Eloquence, IBMTTS ile aynı API’ye sahiptir) ancak lisans sorunları nedeniyle bu sürücüyle Eloquence kullanılması önerilmez. Bu sürücüyle herhangi bir sentez kütüphanesi kullanmadan önce, öncelikle kullanım lisansı haklarını almanız önerilir.

Bu sürücü, web üzerinde herkese açık olarak bulunan IBMTTS dokümantasyonu kullanılarak geliştirilmiştir. Daha fazla ayrıntı için referanslar bölümüne bakın.

## İndirme.

En son sürüm şu bağlantıdan indirilebilir:  
[Sürücüyü bu bağlantıdan indirebilirsiniz.](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## IBMTTS sentezleyicisi nedir?

ViaVoice TTS, IBM tarafından geliştirilmiş bir metin-konuşma motorudur ve insan dilinin metinsel temsilini konuşmaya dönüştürür.

## Özellikler ve ayarlar.

* Ses, varyant, hız, perde, tonlama ve ses seviyesi ayarlarını destekler.
* Ek kafa boyutu, pürüzlülük, nefeslilik parametre ayarlarını destekler. Kendi sesinizi oluşturun!
* Ters tırnak ses etiketlerini etkinleştir veya devre dışı bırak. Şakacılardan gelebilecek kötü amaçlı kodlardan korunmak için devre dışı bırakın, sentezleyici ile birçok eğlenceli şey yapmak için etkinleştirin. Ancak düzgün çalışması için NVDA’da bazı ek ayarlamalar gerekir.
* Hız artırma. Sentezleyici sizin için çok hızlı konuşmuyorsa, bunu etkinleştirin ve maksimum ses hızını elde edin!
* Otomatik dil değiştirme. İşaretlendiğinde metni doğru dilde okumasını sağlayın.
* Kapsamlı filtreleme. Bu sürücü, çökmeleri ve sentezleyicinin diğer garip davranışlarını düzeltmek için kapsamlı bir filtre seti içerir.
* Sözlük desteği. Bu sürücü, her dil için özel kelimeler, kökler ve kısaltmalar için kullanıcı sözlüklerinin entegrasyonunu destekler. Hazır sözlük setleri [the community dictionary repository](https://github.com/eigencrow/IBMTTSDictionaries) veya [mohamed00's alternative repository (with IBM synth dictionaries)](https://github.com/mohamed00/AltIBMTTSDictionaries) adreslerinden elde edilebilir.

### Ek ayarlar:

* Kısaltma genişletmeyi etkinleştir: kısaltmaların genişletilmesini açıp kapatır. Bu seçeneği devre dışı bırakmanın, kullanıcı tarafından sağlanan kısaltma sözlüklerinde belirtilen kısaltmaların genişletilmesini de devre dışı bırakacağını unutmayın.
* Cümle tahminini etkinleştir: bu seçenek etkinleştirildiğinde, sentezleyici cümle yapısına göre duraklamaların nerede olacağını tahmin etmeye çalışır; örneğin "and" veya "the" gibi kelimeleri ifade sınırları olarak kullanarak. Bu seçenek kapalıysa, yalnızca virgül veya benzeri noktalama işaretleriyle karşılaşıldığında duraklar.
* Duraklamalar: Bu üç seçeneğe sahip bir açılır kutudur.
  * Kısaltma yapma: duraklamalar hiçbir şekilde kısaltılmaz ve her durumda IBMTTS’in orijinal duraklamaları kullanılır.
  * Sadece metin sonunda kısalt: nokta ve virgül gibi noktalama işaretlerinin duraklamaları kısaltılmaz, ancak metin sona erdiğinde kısaltılır; örneğin NVDA+t tuşuna hızlıca iki kez basarak bir uygulamanın başlık çubuğunu harf harf hecelemek gibi durumlarda.
  * Tüm duraklamaları kısalt: noktalama duraklamaları ve metin sonundaki duraklamalar dahil tüm duraklamalar kısaltılır.
* Her zaman mevcut konuşma ayarlarını gönder: sentezleyicide konuşma ve perde ayarlarının zaman zaman kısa süreliğine varsayılan değerlere sıfırlanmasına neden olan bir hata vardır. Bu sorunun nedeni şu anda bilinmemektedir, ancak geçici çözüm olarak mevcut konuşma hızı ve perde ayarlarını sürekli göndermektir. Bu seçenek genellikle etkinleştirilmelidir. Ancak ters tırnak ses etiketleri içeren metinler okunurken devre dışı bırakılmalıdır.
* Örnekleme oranı: sentezleyicinin ses kalitesini değiştirir. Özellikle IBMTTS için kullanışlıdır; örnekleme oranını 8 kHz olarak ayarlamak yeni bir ses setine erişim sağlar.

### IBMTTS kategori ayarları.

Bu eklenti, NVDA Ayarlar iletişim kutusu içinde, konuşma senteziyle ilgili olmayan bazı dahili işlevleri yönetmek için kendi ayar kategorisine sahiptir.

* IBMTTS için güncellemeleri otomatik Denetle: Bu seçenek işaretliyse, eklenti her gün yeni sürümleri denetler.
* Güncellemeleri Denetle düğmesi: Yeni eklenti güncellemelerini elle denetler.
* IBMTTS klasör adresi: IBMTTS kütüphanesini yüklemek için yol. Mutlak veya göreli olabilir.
* IBMTTS kütüphane adı (dll): Kütüphanenin adı (dll). Yol eklemeyin, sadece uzantıyla birlikte adı yazın, genellikle ".dll".
* IBMTTS kütüphanesi için gözat... Sistem üzerinde IBMTTS kütüphanesini aramak için dosya seçme penceresi açar. Mutlak yol olarak kaydedilir.
* IBMTTS dosyalarını bir eklentiye kopyala (bazı IBMTTS dağıtımlarında çalışmayabilir): IBMTTS için kütüphane yolu ayarlanmışsa, tüm klasör dosyalarını eciLibraries adlı yeni bir eklentiye kopyalar ve mevcut yolu göreli bir yol olarak günceller. NVDA’nın taşınabilir sürümlerinde çok kullanışlıdır. Yalnızca ses dil bilgileri için "eci.ini" dosyalarını kullanan kütüphanelerle çalışır. Kütüphane Windows kayıt defterini kullanıyorsa bu seçenek çalışmaz.

Not: Otomatik veya manuel güncelleme işlevi eklentinin dahili dosyalarını kaldırmaz. Kütüphanelerinizi bu konumda kullanıyorsanız, bu işlevi güvenle kullanabilirsiniz. Kütüphaneleriniz güvende olacaktır.

## 64-bit Uyumluluk & Mimari

**NVDA 2026** ile birlikte ekran okuyucu 64-bit Python yorumlayıcısına geçmiştir. Yerel 64-bit IBMTTS kütüphaneleri mevcut olmadığından, 64-bit Python ortamı ile mevcut 32-bit IBMTTS kütüphaneleri arasında köprü kurmak için özel bir uyumluluk katmanı uygulanmıştır.

### Uygulama Ayrıntıları

Sorunsuz entegrasyon sağlamak için sürücü aşağıdaki mimariyi kullanır:

* **32-bit DLL Host:** Özel bir Rust 32-bit host, 64-bit süreçler için köprü görevi görür. Bu host gerekli `eci.dll` dosyasını dinamik olarak yükleyebilir.
* **Süreçler Arası İletişim (IPC):**
* **Fonksiyon Çağrıları:** İletişim, mesaj modunda **overlapped named pipes** aracılığıyla sağlanır.
* **Ses Akışı:** Yüksek performanslı ses veri aktarımı, süreçler arasında okuma/yazma işlemlerini sinyallemek için senkronizasyon olayları kullanılarak **paylaşılan bellek** üzerinden yönetilir.
* **Çalıştırma:** Host süreci `rundll32` kullanılarak başlatılır.
* **Python Proxy:** Python tabanlı bir proxy, standart `eci.dll` yerine geçer. Host uç noktalarıyla iletişim kurar ve ses akışını doğrudan paylaşılan bellekten işler.
* **Dinamik Yükleme:** Sürücü ortamı otomatik algılar. Proxy yalnızca **NVDA 64-bit** altında başlatılır; **NVDA 32-bit** altında orijinal `eci.dll` yerel olarak yüklenir.

### 32 bit host bridge

32-bit host’un uygulama ayrıntıları için şu depoya bakın:
[ibmtts-host32-bridge](https://github.com/davidacm/ibmtts-host32-bridge)

## Gereksinimler.

### NVDA.

NVDA 2019.3 veya daha yenisine ihtiyacınız var.

### IBMTTS sentezleyici kütüphaneleri.

Bu sadece sürücüdür, kütüphaneleri başka bir yerden edinmeniz gerekir.
Bu sürücü, Doğu Asya dil desteği ekleyen biraz daha yeni kütüphaneleri destekler ve metnin doğru kodlanması için özel düzeltmeler içerir. Ancak bu özelliklere sahip olmayan eski kütüphaneler de çalışmalıdır.
21.03A1 sürümünden itibaren bu sürücü, sadece SpeechWorks kütüphaneleriyle değil, IBM’in daha yeni kütüphaneleriyle de çalışır. Bu kütüphaneler için bağımsız düzeltmeler eklenmiştir ve ek diller ile diğer farklar dikkate alınmıştır. Concatenative sesler desteklenir ve sesler kurulduktan sonra örnekleme oranı 8 kHz olarak ayarlanarak erişilebilir. En iyi sonuçlar için ibmeci.dll’in Haziran 2005 derlemesini (sürüm 7.0.0.0) kullanın; daha eski sürümler, örneğin listede hızlı gezinirken olduğu gibi metin hızlı geldiğinde kararsız olabilir. Ayrıca Hong Kong Kantoncası veya Çince IBMTTS kütüphanelerini kullanıyorsanız, bazı karakterlerin içsel olarak dönüştürüldüğü pinyin ile hecelenmesini önlemek için, destekleniyorsa “yazım işlevini kullan” seçeneğini devre dışı bırakmak isteyebilirsiniz.

## Kurulum.

NVDA eklentisi olarak yükleyin. Ardından NVDA ayarlarını açın ve IBMTTS kategorisinde IBMTTS klasör dosyalarını ayarlayın.
Ayrıca bu kategoride harici IBMTTS dosyalarını bir eklentiye kopyalayarak yerel olarak da kullanabilirsiniz.

## Çeviriye katkıda bulunma.

İşinizi kolaylaştırmak için master dalında bir
[translation template in the master branch.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)

Dokümantasyon için ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) adlı bir dosya oluşturdum.
Bu dosyayı kullanarak dokümantasyonda nelerin değiştiğini görebilir ve kendi diliniz için güncelleyebilirsiniz.

Bu eklentiyi başka bir dile çevirmek istiyorsanız ve github hesabı açmak ya da python ve diğer araçları kurmak istemiyorsanız, aşağıdaki adımları izleyin:

1. Hedef dil için temel olarak
   [bu şablonu](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot) kullanın.
2. ["poedit"](https://poedit.net/) indirin,
bu yazılım çeviri dizelerini yönetmenize yardımcı olur.
3. Dokümantasyonu da çevirmek istiyorsanız, yeni değişiklikleri
[at this link.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) adresinden görebilirsiniz. Tüm İngilizce dokümantasyonu [Tam İngilizce belgeler burada.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Çeviriyi bitirdiğinizde bana şu adrese gönderebilirsiniz: "[dhf360@gmail.com](mailto:dhf360@gmail.com)".

Kaynak dosyaları derlemeniz gerekmez. Yeni bir eklenti sürümü yayınlanırken bunu ben yapacağım. İlgili commit’te adınızı belirteceğim. Eğer adınızın belirtilmesini istemiyorsanız, bunu e-postada belirtin.

Not: En güncel çeviri şablonunu kullandığınızdan emin olun.

Bu alternatif bir yöntemdir. İsterseniz her zaman normal yolu da izleyebilirsiniz. Bu repo’yu fork edip, kendi diliniz için çeviriyi güncelleyip PR gönderebilirsiniz. Ancak bu yöntem sizin için daha karmaşık olacaktır.

## Dağıtım için paketleme.

1. Python kurun, şu anda python 3.7 kullanılıyor, ancak daha yeni bir sürüm de kullanabilirsiniz.
2. gettext kurun, Windows için dağıtımı [this link.](https://mlocati.github.io/articles/gettext-iconv-windows.html) adresinden indirebilirsiniz. Windows 64 bit kullanıyorsanız [bu sürüm.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe) önerilir.
3. (isteğe bağlı ama önerilir) NVDA eklentilerini yönetmek için bir python sanal ortamı oluşturun. Konsolda "python -m venv PAT_TO_FOLDER" komutunu kullanın. PAT_TO_FOLDER, sanal ortam için istediğiniz yol olmalıdır.
4. 2. adımı yaptıysanız, PAT_TO_FOLDER içine gidin ve scripts klasörü içinde "activate" komutunu çalıştırın. Ortam adı konsol isteminde görünmelidir.
5. Bu repo’yu istediğiniz konuma klonlayın: "git klonu [https://github.com/davidacm/NVDA-IBMTTS-Driver.git](https://github.com/davidacm/NVDA-IBMTTS-Driver.git)".
6. Aynı konsolda bu Depo’nun klasörüne gidin.
7. Gereksinimleri yükleyin: "pip install -r requirements.txt".
8. scons komutunu çalıştırın. Hata yoksa oluşturulan eklenti bu repo’nun kök dizinine yerleştirilir.

Konsolu kapattığınızda sanal ortam devre dışı bırakılır.

### Kütüphaneleri bağımsız bir eklenti olarak paketleme.

Kütüphaneleri bu sürücüyle birlikte dahil etmek önerilmez. Bunun nedeni, kullanıcı sürücüyü
[resmi depo](https://github.com/davidacm/NVDA-IBMTTS-Driver) üzerinden NVDA eklenti yükleyicisi ile güncellediğinde, eski sürümün kütüphaneler dahil silinecek olmasıdır. Bunun bir çözümü, kütüphaneleri ayrı bir eklentiye kurmaktır.
[Bu bağlantıyı takip edin](https://github.com/davidacm/ECILibrariesTemplate) bağlantısından kütüphaneleri ayrı bir eklenti olarak nasıl paketleyeceğinizi öğrenebilirsiniz.

### Notlar:

* Dahili güncelleme özelliğini (manuel veya otomatik) kullanırsanız, kütüphaneler eklenti içinde olsa bile silinmez.
* Sentezleyici eklenti içinde veya
  ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate) eklentisinde bulunuyorsa, sürücü ini kütüphane yollarını otomatik olarak günceller. Böylece taşınabilir NVDA sürümlerinde kullanabilirsiniz.
* "IBMTTS dosyalarını bir eklentiye kopyala" düğmesini kullandığınızda yeni bir eklenti oluşturulur. Bu nedenle IBMTTS’i kaldırmak isterseniz iki eklentiyi kaldırmanız gerekir: "IBMTTS driver" ve "Eci libraries".
* Bu projede scons ve gettext araçları yalnızca python 3 ile uyumludur. Python 2.7 ile çalışmaz.
* Ek IBMTTS gerekli dosyalarını eklenti içine koyabilirsiniz (yalnızca kişisel kullanım için). Bunları "addon\synthDrivers\ibmtts" klasörüne kopyalayın. Gerekirse "settingsDB.py" içinde varsayılan kütüphane adını ayarlayın.
* Yapılandırılmış kütüphane yolu göreli değilse, bu eklenti "eci.ini" dosyasındaki yolları güncellemez. Sürücü, mutlak yollar kullanıldığında yolların doğru olduğunu varsayar ve güncelleme yapmaz. Kütüphane yolunu ayarlarken bunu göz önünde bulundurun. Yanlışsa, bu durum NVDA’nın bu sentezleyici ile konuşamamasına neden olabilir.

## Sorun bildirme:

Bu sürücüyle uyumlu bazı kütüphanelerde bir güvenlik açığı bulursanız, sorun çözülmeden önce lütfen GitHub’da issue açmayın veya forumlarda paylaşmayın. Lütfen sorunu
[bu formda.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit) üzerinden bildirin.

Sorun sürücüyü veya ekran okuyucuyu çökertmiyorsa, buradan bir GitHub sorunu açın:
[github sorunu burada.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referanslar.

Bu sürücü IBM TTS SDK üzerine kuruludur, dokümantasyon şu adreste mevcuttur:
[bu bağlantı](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

ayrıca Columbia Üniversitesi’nde de:
[bu bağlantı](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Veya şu repodan bir yedek kopya alabilirsiniz:
[Bu depo](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Peter Parente tarafından geliştirilen IBM TTS için Python sarmalayıcı](https://sourceforge.net/projects/ibmtts-sdk/)

Yedek dosyalar için buraya bakın:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

veya [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
