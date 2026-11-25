
from io import BytesIO

from PIL import Image
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDict

from .forms import PronaForm
from .models import (
    Perdorues,
    Prona,
    Klienti,
    Kerkesa,
    MesazhKontakti,
)


class PronaFormTests(SimpleTestCase):

    def setUp(self):
        self.te_dhenat = {
            "lloji": "banese",
            "qyteti": "Prizren",
            "cmimi": "85000",
            "siperfaqja": "85",
            "status": "e_lire",
        }

    def krijo_foto(self, emri="prona.png", formati="PNG"):
        skedari = BytesIO()

        Image.new(
            "RGB",
            (100, 100),
            color="white"
        ).save(skedari, format=formati)

        return SimpleUploadedFile(
            emri,
            skedari.getvalue(),
            content_type=f"image/{formati.lower()}"
        )

    def test_01_prona_e_vlefshme(self):
        forma = PronaForm(data=self.te_dhenat)
        self.assertTrue(forma.is_valid(), forma.errors)

    def test_02_qyteti_me_numra(self):
        self.te_dhenat["qyteti"] = "12345"
        forma = PronaForm(data=self.te_dhenat)
        self.assertFalse(forma.is_valid())
        self.assertIn("qyteti", forma.errors)

    def test_03_pastrimi_i_qytetit(self):
        self.te_dhenat["qyteti"] = "  Fushe   Kosove  "
        forma = PronaForm(data=self.te_dhenat)
        self.assertTrue(forma.is_valid(), forma.errors)
        self.assertEqual(
            forma.cleaned_data["qyteti"],
            "Fushe Kosove"
        )

    def test_04_cmimi_negativ(self):
        self.te_dhenat["cmimi"] = "-500"
        forma = PronaForm(data=self.te_dhenat)
        self.assertFalse(forma.is_valid())
        self.assertIn("cmimi", forma.errors)

    def test_05_siperfaqja_zero(self):
        self.te_dhenat["siperfaqja"] = "0"
        forma = PronaForm(data=self.te_dhenat)
        self.assertFalse(forma.is_valid())
        self.assertIn("siperfaqja", forma.errors)

    def test_06_fotografia_png(self):
        forma = PronaForm(
            data=self.te_dhenat,
            files={"foto": self.krijo_foto()}
        )
        self.assertTrue(forma.is_valid(), forma.errors)

    def test_07_fotografia_gif(self):
        forma = PronaForm(
            data=self.te_dhenat,
            files={
                "foto": self.krijo_foto("prona.gif", "GIF")
            }
        )
        self.assertFalse(forma.is_valid())
        self.assertIn("foto", forma.errors)

    def test_08_fotografia_e_pavlefshme(self):
        foto = SimpleUploadedFile(
            "prona.png",
            b"Skedar i pavlefshem",
            content_type="image/png"
        )

        forma = PronaForm(
            data=self.te_dhenat,
            files={"foto": foto}
        )

        self.assertFalse(forma.is_valid())
        self.assertIn("foto", forma.errors)

    def test_09_galeria_me_kater_foto(self):
        fotot = [
            self.krijo_foto(f"foto_{i}.png")
            for i in range(4)
        ]

        forma = PronaForm(
            data=self.te_dhenat,
            files=MultiValueDict({
                "fotot_shtese": fotot
            })
        )

        self.assertTrue(forma.is_valid(), forma.errors)
        self.assertEqual(
            len(forma.cleaned_data["fotot_shtese"]),
            4
        )

    def test_10_galeria_me_nente_foto(self):
        fotot = [
            self.krijo_foto(f"foto_{i}.png")
            for i in range(9)
        ]

        forma = PronaForm(
            data=self.te_dhenat,
            files=MultiValueDict({
                "fotot_shtese": fotot
            })
        )

        self.assertFalse(forma.is_valid())
        self.assertIn("fotot_shtese", forma.errors)

    def test_11_galeria_me_gif(self):
        forma = PronaForm(
            data=self.te_dhenat,
            files=MultiValueDict({
                "fotot_shtese": [
                    self.krijo_foto("foto.gif", "GIF")
                ]
            })
        )

        self.assertFalse(forma.is_valid())
        self.assertIn("fotot_shtese", forma.errors)

    def test_12_fotografia_mbi_pese_mb(self):
        foto = self.krijo_foto()

        permbajtja = (
            foto.read()
            + b"\0" * (6 * 1024 * 1024)
        )

        foto_e_madhe = SimpleUploadedFile(
            "prona.png",
            permbajtja,
            content_type="image/png"
        )

        forma = PronaForm(
            data=self.te_dhenat,
            files={"foto": foto_e_madhe}
        )

        self.assertFalse(forma.is_valid())
        self.assertIn("foto", forma.errors)


class SmartEstateTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.administratori = Perdorues.objects.create_user(
            username="admin_test",
            password="TestAdmin2026!",
            emri="Administratori Test",
            roli="administrator"
        )

        cls.agjenti = Perdorues.objects.create_user(
            username="agjent_test",
            password="TestAgjent2026!",
            emri="Agjenti Test",
            roli="agjent"
        )

        cls.agjenti_tjeter = Perdorues.objects.create_user(
            username="agjent_tjeter",
            password="TestAgjent2026!",
            emri="Agjenti Tjeter",
            roli="agjent"
        )

        cls.prona = Prona.objects.create(
            agjent=cls.agjenti,
            lloji="banese",
            qyteti="Prizren",
            cmimi=85000,
            siperfaqja=85,
            status="e_lire"
        )

        cls.prona_tjeter = Prona.objects.create(
            agjent=cls.agjenti_tjeter,
            lloji="shtepi",
            qyteti="Prishtine",
            cmimi=150000,
            siperfaqja=200,
            status="e_lire"
        )

        cls.klienti = Klienti.objects.create(
            emri="Klienti Test",
            kontakti="049123456"
        )

    def te_dhenat_prones(self):
        return {
            "lloji": "banese",
            "qyteti": "Peje",
            "cmimi": "65000",
            "siperfaqja": "75",
            "status": "e_lire",
        }

    def te_dhenat_interesimit(self):
        return {
            "emri": "Klienti Shembull",
            "telefoni": "049123456",
            "email": "klienti@example.com",
            "mesazhi": "Jam i interesuar per kete prone.",
        }

    def te_dhenat_kontaktit(self):
        return {
            "emri": "Vizitori Test",
            "email": "vizitori@example.com",
            "subjekti": "Informacion per pronat",
            "mesazhi": "Deshiroj informacion shtese per pronat.",
        }

    def test_13_hyrja_administratorit(self):
        pergjigjja = self.client.post(
            reverse("hyrja"),
            {
                "username": "admin_test",
                "password": "TestAdmin2026!",
            }
        )

        self.assertRedirects(
            pergjigjja,
            reverse("paneli"),
            fetch_redirect_response=False
        )
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.administratori.pk)
        )

    def test_14_hyrja_agjentit(self):
        pergjigjja = self.client.post(
            reverse("hyrja"),
            {
                "username": "agjent_test",
                "password": "TestAgjent2026!",
            }
        )

        self.assertRedirects(
            pergjigjja,
            reverse("paneli"),
            fetch_redirect_response=False
        )
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.agjenti.pk)
        )

    def test_15_fjalekalimi_i_gabuar(self):
        pergjigjja = self.client.post(
            reverse("hyrja"),
            {
                "username": "admin_test",
                "password": "gabim123",
            }
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )
        self.assertTrue(pergjigjja.context["gabimi"])

    def test_16_dalja_nga_sistemi(self):
        self.client.force_login(self.administratori)

        pergjigjja = self.client.post(reverse("dalja"))

        self.assertRedirects(
            pergjigjja,
            reverse("hyrja"),
            fetch_redirect_response=False
        )
        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

    def test_17_paneli_pa_autentikim(self):
        pergjigjja = self.client.get(reverse("paneli"))

        self.assertRedirects(
            pergjigjja,
            reverse("hyrja") + "?next=" + reverse("paneli"),
            fetch_redirect_response=False
        )

    def test_18_administratori_sheh_te_gjitha_pronat(self):
        self.client.force_login(self.administratori)

        pergjigjja = self.client.get(reverse("paneli"))

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertEqual(
            pergjigjja.context["numri_pronave"],
            2
        )

    def test_19_agjenti_sheh_pronat_e_veta(self):
        self.client.force_login(self.agjenti)

        pergjigjja = self.client.get(reverse("paneli"))

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertEqual(
            pergjigjja.context["numri_pronave"],
            1
        )

    def test_20_agjenti_nuk_ndryshon_pronen_e_tjetrit(self):
        self.client.force_login(self.agjenti)

        pergjigjja = self.client.post(
            reverse(
                "ndrysho_prone",
                args=[self.prona_tjeter.pk]
            ),
            self.te_dhenat_prones()
        )

        self.assertEqual(pergjigjja.status_code, 404)

        self.prona_tjeter.refresh_from_db()
        self.assertEqual(
            self.prona_tjeter.qyteti,
            "Prishtine"
        )

    def test_21_filtrimi_sipas_qytetit(self):
        pergjigjja = self.client.get(
            reverse("pronat"),
            {"qyteti": "Prizren"}
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertQuerySetEqual(
            pergjigjja.context["pronat"],
            [self.prona]
        )

    def test_22_filtrimi_sipas_llojit(self):
        pergjigjja = self.client.get(
            reverse("pronat"),
            {"lloji": "shtepi"}
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertQuerySetEqual(
            pergjigjja.context["pronat"],
            [self.prona_tjeter]
        )

    def test_23_filtrimi_sipas_cmimit(self):
        pergjigjja = self.client.get(
            reverse("pronat"),
            {
                "cmimi_min": "50000",
                "cmimi_max": "100000",
            }
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertQuerySetEqual(
            pergjigjja.context["pronat"],
            [self.prona]
        )

    def test_24_filtrimi_me_cmim_te_pavlefshem(self):
        pergjigjja = self.client.get(
            reverse("pronat"),
            {"cmimi_min": "abc"}
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertTrue(
            pergjigjja.context["gabim_cmimi"]
        )

    def test_25_shtimi_i_prones(self):
        self.client.force_login(self.agjenti)

        pergjigjja = self.client.post(
            reverse("shto_prone"),
            self.te_dhenat_prones()
        )

        prona = Prona.objects.get(qyteti="Peje")

        self.assertRedirects(
            pergjigjja,
            reverse("detajet_prones", args=[prona.pk]),
            fetch_redirect_response=False
        )
        self.assertEqual(prona.agjent, self.agjenti)

    def test_26_ndryshimi_i_prones(self):
        self.client.force_login(self.agjenti)

        te_dhenat = self.te_dhenat_prones()
        te_dhenat["cmimi"] = "90000"

        pergjigjja = self.client.post(
            reverse(
                "ndrysho_prone",
                args=[self.prona.pk]
            ),
            te_dhenat
        )

        self.assertRedirects(
            pergjigjja,
            reverse(
                "detajet_prones",
                args=[self.prona.pk]
            ),
            fetch_redirect_response=False
        )

        self.prona.refresh_from_db()
        self.assertEqual(self.prona.cmimi, 90000)

    def test_27_fshirja_e_prones(self):
        self.client.force_login(self.agjenti)

        pergjigjja = self.client.post(
            reverse(
                "fshi_prone",
                args=[self.prona.pk]
            )
        )

        self.assertRedirects(
            pergjigjja,
            reverse("paneli"),
            fetch_redirect_response=False
        )

        self.assertFalse(
            Prona.objects.filter(
                pk=self.prona.pk
            ).exists()
        )

    def test_28_shtimi_i_klientit(self):
        self.client.force_login(self.administratori)

        pergjigjja = self.client.post(
            reverse("shto_klient"),
            {
                "emri": "Klient i Ri",
                "kontakti": "044123456",
            }
        )

        self.assertRedirects(
            pergjigjja,
            reverse("klientet"),
            fetch_redirect_response=False
        )
        self.assertTrue(
            Klienti.objects.filter(
                emri="Klient i Ri"
            ).exists()
        )

    def test_29_ndryshimi_i_klientit(self):
        self.client.force_login(self.administratori)

        pergjigjja = self.client.post(
            reverse(
                "ndrysho_klient",
                args=[self.klienti.pk]
            ),
            {
                "emri": "Klienti i Perditesuar",
                "kontakti": "045123456",
            }
        )

        self.assertRedirects(
            pergjigjja,
            reverse("klientet"),
            fetch_redirect_response=False
        )

        self.klienti.refresh_from_db()
        self.assertEqual(
            self.klienti.emri,
            "Klienti i Perditesuar"
        )

    def test_30_fshirja_e_klientit(self):
        self.client.force_login(self.administratori)

        pergjigjja = self.client.post(
            reverse(
                "fshi_klient",
                args=[self.klienti.pk]
            )
        )

        self.assertRedirects(
            pergjigjja,
            reverse("klientet"),
            fetch_redirect_response=False
        )

        self.assertFalse(
            Klienti.objects.filter(
                pk=self.klienti.pk
            ).exists()
        )

    def test_31_interesimi_per_pronen(self):
        pergjigjja = self.client.post(
            reverse(
                "dergo_interesimin",
                args=[self.prona.pk]
            ),
            self.te_dhenat_interesimit()
        )

        self.assertRedirects(
            pergjigjja,
            reverse(
                "detajet_prones",
                args=[self.prona.pk]
            ),
            fetch_redirect_response=False
        )

        self.assertTrue(
            Kerkesa.objects.filter(
                prona=self.prona,
                email="klienti@example.com",
                klienti__emri="Klienti Shembull"
            ).exists()
        )

    def test_32_interesimi_me_email_te_gabuar(self):
        te_dhenat = self.te_dhenat_interesimit()
        te_dhenat["email"] = "emailgabim"

        pergjigjja = self.client.post(
            reverse(
                "dergo_interesimin",
                args=[self.prona.pk]
            ),
            te_dhenat
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertEqual(Kerkesa.objects.count(), 0)
        self.assertIn(
            "email",
            pergjigjja.context["interesimi_form"].errors
        )

    def test_33_dergimi_i_mesazhit(self):
        pergjigjja = self.client.post(
            reverse("kontakt"),
            self.te_dhenat_kontaktit()
        )

        self.assertRedirects(
            pergjigjja,
            reverse("kontakt"),
            fetch_redirect_response=False
        )

        self.assertTrue(
            MesazhKontakti.objects.filter(
                email="vizitori@example.com"
            ).exists()
        )

    def test_34_kontakti_me_mesazh_te_shkurter(self):
        te_dhenat = self.te_dhenat_kontaktit()
        te_dhenat["mesazhi"] = "Hi"

        pergjigjja = self.client.post(
            reverse("kontakt"),
            te_dhenat
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertEqual(
            MesazhKontakti.objects.count(),
            0
        )
        self.assertIn(
            "mesazhi",
            pergjigjja.context["form"].errors
        )

    def test_35_faqja_kryesore(self):
        pergjigjja = self.client.get(reverse("home"))
        self.assertEqual(pergjigjja.status_code, 200)

    def test_36_faqja_pronat(self):
        pergjigjja = self.client.get(reverse("pronat"))
        self.assertEqual(pergjigjja.status_code, 200)

    def test_37_faqja_rreth_nesh(self):
        pergjigjja = self.client.get(reverse("rreth_nesh"))
        self.assertEqual(pergjigjja.status_code, 200)

    def test_38_faqja_sherbimet(self):
        pergjigjja = self.client.get(reverse("sherbimet"))
        self.assertEqual(pergjigjja.status_code, 200)

    def test_39_faqja_kontakt(self):
        pergjigjja = self.client.get(reverse("kontakt"))
        self.assertEqual(pergjigjja.status_code, 200)

    def test_40_detajet_e_prones(self):
        pergjigjja = self.client.get(
            reverse(
                "detajet_prones",
                args=[self.prona.pk]
            )
        )

        self.assertEqual(pergjigjja.status_code, 200)
        self.assertEqual(
            pergjigjja.context["prona"],
            self.prona
        )
