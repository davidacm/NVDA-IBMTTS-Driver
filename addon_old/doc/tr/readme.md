# IBMTTS sürücüsü, NVDA için Eklenti #

  Bu eklenti, IBMTTS sentezleyici ile NVDA uyumluluğunu sağlar.  
  IBMTTS kitaplıklarını dağıtamıyoruz. Yani bu sadece sürücü.  
  Bu sürücüyü geliştirmek istiyorsanız, çekme isteklerinizi göndermekten çekinmeyin!  

Bu sürücü Eloquence kitaplıklarıyla uyumlu olsa da (Eloquence, IBMTTS ile aynı api'ye sahip olduğundan) lisans sorunları nedeniyle Eloquence'ın bu sürücüyle kullanılması önerilmez. Bu sürücü ile herhangi bir sentezleyici kitaplığını kullanmadan önce lisans kullanım haklarını almanız önerilir.  

Bu sürücü, IBMTTS için web'de halka açık olan belgelerle geliştirilmiştir. Daha fazla ayrıntı için referanslar bölümüne bakın.  

## İndirme.
En son sürüm [bu bağlantıdan indirilebilir](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## IBMTTS sentezleyici nedir?

ViaVoice TTS, IBM tarafından geliştirilen ve insan dilinin metinsel temsilini konuşmaya dönüştüren bir metinden konuşmaya motorudur.

## Özellikler ve ayarlar.

* Ses, varyant, hız, perde, çekim ve ses ayarı desteği.
* Ekstra kafa boyutu, Pürüzlülük, Nefes alma parametreleri ayarları desteği. Kendi sesini yarat!
* Ters alıntı ses etiketlerini etkinleştirin veya devre dışı bırakın. Kendinizi şakacılardan gelen kötü amaçlı kodlardan korumak için devre dışı bırakın, sentezleyici ile birçok eğlenceli şey yapmasını etkinleştirin. Düzgün çalışması için NVDA ile biraz daha ince ayar yapılması gerekiyor.
* Hız artışı. Sentezleyici sizinle çok hızlı konuşmuyorsa etkinleştirin ve maksimum ses hızını elde edin!
* otomatik dil değiştirme. İşaretlendiğinde sentezleyicinin metni size doğru dilde okumasına izin verir.
* kapsamlı filtreleme Bu sürücü, sentezleyicinin çökmelerini ve diğer garip davranışlarını düzeltmek için kapsamlı bir filtre seti içerir.
* sözlük desteği. Bu sürücü, her dil için özel kelimelerin, köklerin ve kısaltma kullanıcı sözlüklerinin entegrasyonunu destekler. Hazır sözlük setleri, [topluluk sözlük deposundan](https://github.com/thunderdrop/IBMTTSDictionaries) veya [mohamed00'in alternatif deposundan (IBM synth sözlükleriyle)](https://github.com/mohamed00) elde edilebilir.

### Ek ayarlar:

* Kısaltma genişletmeyi etkinleştir: kısaltmaların genişletilmesini değiştirir. Bu seçeneği devre dışı bırakmanın, kullanıcı tarafından sağlanan kısaltma sözlüklerinde belirtilen kısaltmaların genişletilmesini de devre dışı bırakacağını unutmayın.
* Tümce tahminini etkinleştir: Bu seçenek etkinleştirilirse, sentezleyici, örneğin "ve" veya "the" gibi sözcükleri tümce sınırları olarak kullanarak yapılarına göre cümlelerde duraklamaların nerede olacağını tahmin etmeye çalışır. Bu seçenek kapalıysa, yalnızca virgül veya benzeri noktalama işaretleriyle karşılaşıldığında duraklar.
* Duraklamaları kısaltın: diğer ekran okuyucularda görülenler gibi daha kısa noktalama duraklamaları için bu seçeneği etkinleştirin.
* Her zaman geçerli konuşma ayarlarını gönder: Sentezleyicide, konuşma ve perde ayarlarının zaman zaman kısa süreliğine varsayılan değerlerine sıfırlanmasına neden olan bir hata vardır. Bu sorunun nedeni şu anda bilinmiyor, ancak geçici bir çözüm, geçerli konuşma hızını ve perde ayarlarını sürekli olarak göndermektir. Bu seçenek genellikle etkinleştirilmelidir. Ancak, ters alıntı ses etiketleri içeren metin okunurken devre dışı bırakılmalıdır.
* Örnekleme hızı: sentezleyicinin ses kalitesini değiştirir. Örnek hızının 8 kHz olarak ayarlanmasının yeni bir ses grubuna erişim sağladığı IBMTTS için en kullanışlıdır.

### IBMTTS kategori ayarları.

Bu eklentinin, konuşma senteziyle ilgili olmayan bazı dahili işlevleri yönetmek için NVDA Terciler iletişim kutusu içinde kendi ayar kategorisi vardır.

* IBMTTS için güncellemeleri otomatik olarak denetle: Bu seçenek işaretlenirse, eklenti mevcut yeni sürümleri günlük olarak kontrol eder.
* Güncellemeleri Denetle düğmesi: Güncellemeleri el ile denetleme imkanı verir.
* IBMTTS klasör adresi: IBMTTS kitaplığını yükleme yolu. Mutlak veya göreceli olabilir.
* IBMTTS kitaplık adı (dll): Kitaplığın adı (dll). Yolları dahil etmeyin, yalnızca uzantılı ad, genellikle ".dll".
* BirIBMTTS kitaplığı Bul... Sistemde IBMTTS kitaplığını aramak için bir dosya gözat iletişim kutusu açar. Mutlak bir yol olarak kaydedilecektir.
* IBMTTS dosyalarını bir eklentide kopyalayın (bazı IBMTTS dağıtımları için çalışmayabilir): IBMTTS için kitaplık yolu ayarlanmışsa, tüm klasör dosyalarını eciLibraries adlı yeni bir eklentiye kopyalar ve mevcut yolu bir göreceli yol. NVDA'nın taşınabilir sürümlerinde çok kullanışlıdır. Yalnızca sesli dil bilgileri için "eci.ini" dosyalarını kullanan kitaplıklar için çalışır. Kitaplık Windows kayıt defterini kullanıyorsa bu seçenek çalışmaz.

Not: Otomatik veya manuel güncelleme işlevi, eklentinin dahili dosyalarını kaldırmaz. O yerdeki kitaplıklarınızı kullanırsanız, bu işlevi güvenle kullanabilirsiniz. Kitaplıklarınız güvende olacak.

## Gereksinimler.
### NVDA.
  NVDA 2019.3 veya sonrasına ihtiyacınız var.

### IBMTTS sentezleyici kitaplıkları.
  Bu sadece sürücü, kütüphaneleri başka bir yerden almalısınız.  
  Bu sürücü, Doğu Asya dili desteği ekleyen biraz daha yeni kitaplıkları destekler ve metnin uygun şekilde kodlanması için özel düzeltmelere sahiptir. Yine de, bunun olmadığı eski kütüphaneler çalışmalıdır.
  21.03A1 sürümünden itibaren bu sürücü, yalnızca SpeechWorks kitaplıkları yerine IBM'in daha yeni kitaplıklarıyla da çalışır. Bu kitaplıklar için bir dizi bağımsız düzeltme dahil edilmiştir ve ek diller ve diğer farklılıklar hesaba katılmıştır. Art arda gelen sesler desteklenir ve sesler yüklendikten sonra örnekleme hızı 8 kHz olarak ayarlanarak erişilebilir. En iyi sonuçları elde etmek için, ibmeci.dll'nin 7.0.0.0 sürümünün Haziran 2005 derlemesini kullanın, çünkü eski sürümler hızlı bir şekilde metin alırken, örneğin bir listedeki öğeler arasında hızla gezinirken, kararsız olabilir.

## Kurulum.
Sadece bir NVDA eklentisi olarak kurun. Daha sonra NVDA Konuşma ayarlarını açın ve IBMTTS klasöründeki dosyaları IBMTTS kategorisinde ayarlayın.
  Ayrıca bu kategoride, harici IBMTTS dosyalarını yerel olarak kullanmak için bir Eklentiye kopyalayabilirsiniz.

## Çeviriye katkıda bulunmak.

İşinizi kolaylaştırmak için bir not bıraktım.
[ana şubedeki çeviri şablonu.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Bu eklentiyi başka bir dile çevirmek istiyor ve github hesabı açmak ya da çeviri için gerekli python ve diğer araçları yüklemek istemiyorsanız aşağıdaki adımları uygulayın:

1. Aşağıdaki bağlantıdan
[bu şablonu](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot),
hedef dil için bir temel olarak kullanın.
2. Bağlantıdan
["poedit" programını indirin](https://poedit.net/),
bu yazılım, çeviri dizilerini yönetmenize yardımcı olacaktır.
3. Belgeleri de çevirmek istiyorsanız,
[İngilizce belgeler bu bağlantıda.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/README.md)
4. Çeviriyi bitirdikten sonra bana <dhf360@gmail.com> adresine gönderebilirsiniz.

Kaynak dosyaları derlemeniz gerekmez. Yeni bir eklenti sürümü yayınlarken yapacağım. Adınızı ilgili taahhütte belirteceğim. Adınızın açıklanmasını istemiyorsanız, bana e-posta ile belirtebilirsiniz.  

Not: En son çeviri dizeleri şablonunu kullandığınızdan emin olun.  

Bu alternatif bir yöntemdir. Eğer isterseniz, her zamanki yoldan gidebilirsiniz. Bu depoyu çatallayın, çeviriyi kendi dilinize göre güncelleyin ve bana bir PR gönderin. Ancak bu yol, sizin için daha fazla karmaşıklık katacaktır.

## Dağıtım için paketleme.

1. Python'u yükleyin, şu anda python 3.7 kullanılıyor, ancak daha yeni bir sürüm kullanabilirsiniz.
2. Gettext'i yükleyin, [bu bağlantıdan Windows için bir dağıtım indirebilirsiniz.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Windows 64 bit kullanıyorsanız, [bu sürümü tavsiye ederim.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (isteğe bağlı ancak önerilen adım) NVDA eklentilerini yönetmek için kullanılacak bir python sanal ortamı oluşturun. Konsolda "python -m venv PAT_TO_FOLDER" kullanın. PAT_TO_FOLDER, sanal ortam için istediğiniz yolun yoludur.
4. 2. adımı yaptıysanız, PAT_TO_FOLDER'a gidin ve betikler klasörü içinde "etkinleştir" komutunu çalıştırın. Ortamın adı konsol prontunda gösterilmelidir.
5. Bu repoyu istediğiniz yola kopyalayın: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Aynı konsol örneğinde, bu deponun klasörüne gidin.
7. Gereksinimleri yükleyin: "pip install -r requirements.txt".
8. scons komutunu çalıştırın. Oluşturulan eklenti, herhangi bir hata yoksa, bu deponun kök dizinine yerleştirilir.

Konsolu kapattığınızda sanal ortam devre dışı kalır.

### Kitaplıkları bağımsız bir eklenti olarak paketleyin.

Kitaplıkların bu sürücüye dahil edilmesi önerilmez. Bunun nedeni, kullanıcının sürücüyü sürücüden güncellemesidir.
[resmi repo](https://github.com/davidacm/NVDA-IBMTTS-Driver),
NVDA eklenti yükleyicisi kullanılarak, kitaplıklar da dahil olmak üzere eski sürüm silinir. Bunun için bir çözüm, kitaplıkları ayrı bir eklentiye yüklemektir.
[Bu bağlantıdaki yönergeleri takip ederek](https://github.com/davidacm/ECILibrariesTemplate)
kitaplıkları ayrı bir eklentide nasıl paketleyeceğinizi öğrenebilirsiniz.

### notlar:

* Dahili güncelleme özelliğini (el ile veya otomatik) kullanırsanız, kitaplıklar eklenti içinde olsalar bile silinmez.
* sentezleyici eklentinin içindeyse veya
["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate)
eklenti, sürücü ini kitaplığı yollarını otomatik olarak güncelleyecektir. Böylece taşınabilir NVDA sürümlerinde kullanabilirsiniz.
* "IBMTTS dosyalarını bir eklentiye kopyala" düğmesini kullandığınızda, yeni bir eklenti oluşturacaktır. Dolayısıyla, IBMTTS'yi kaldırmak istiyorsanız, iki eklentiyi kaldırmanız gerekir: "IBMTTS sürücüsü" ve "Eci kitaplıkları".
* bu projedeki scons ve gettext araçları yalnızca python 3 ile uyumludur. piton 2.7 ile çalışmaz.
* Ek IBMTTS gerekli dosyalarını eklentiye koyabilirsiniz (yalnızca kişisel kullanım için). Bunları "addon\synthDrivers\ibmtts" klasörüne kopyalamanız yeterlidir. Gerekirse "settingsDB.py" içindeki varsayılan kitaplık adını ayarlayın.

## Sorun raporlama:

Bu sürücüyle uyumlu bazı kitaplıklarda bir güvenlik sorunu bulursanız, lütfen Bir github sorunu açın veya sorun çözülmeden önce forumlarda yorum yapın. Lütfen sorunu [bu formda bildirin.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Sorun, sürücüyü veya ekran okuyucuyu çökertmezse, buradan bir [github sorunu açın.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referanslar.
Bu sürücü, IBM tts sdk'yi temel alır, belgeler şu adreste bulunur:
[İlgili bağlantı](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

ayrıca columbia üniversitesinde
[bu bağlantı](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Veya [bu repo üzerinden bir yedek kopya alabilirsiniz.](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Peter Parente tarafından geliştirilen IBM TTS için Python sarıcı](https://sourceforge.net/projects/ibmtts-sdk/)

Buradaki yedekleme dosyalarına bakın:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
veya [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
