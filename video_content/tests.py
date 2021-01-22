""""
Test for the App: video-content
"""
from django.test import Client
from django.test import TestCase
from video_content.models import Video
from details_page.models import Era


class VideoTestCases(TestCase):
    """
    Testcases for the functions in the model 'Video'
    """
    def setUp(self):
        """
        Creating Eras to test video model
        """
        self.frühzeit = Era.objects.create(name='Frühzeit')
        self.archaik = Era.objects.create(name='Archaik')
        self.helenismus = Era.objects.create(name='Helenismus')
        self.römisch = Era.objects.create(name='Römische Kaiserzeit')
        self.klassik = Era.objects.create(name='Klassik')
        self.spätantike = Era.objects.create(name='Spätantike')
        self.sonstiges = Era.objects.create(name='Sonstiges')

    def test1_get_intro_era(self):
        """
        Testing get_intro  and get_era function
        Testcase where there is no video
        """
        self.assertEqual(Video.get_intro(Video), Video.DoesNotExist)
        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list())
        self.assertEqual(list(Video.get_era(Video, 'Frühzeit')), list())
        self.assertEqual(list(Video.get_era(Video, 'Helenismus')), list())
        self.assertEqual(list(Video.get_era(Video, 'Römische Kaiserzeit')), list())
        self.assertEqual(list(Video.get_era(Video, 'Klassik')), list())
        self.assertEqual(list(Video.get_era(Video, 'Spätantike')), list())
        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list())

    def test2_get_intro(self):

        """
        Testing get_intro function
        Testcase where there is only one intro-video
        """
        Video.objects.create(title='Intro1', video='/media/videos/Intro.mp4', era=self.sonstiges, intro=True)
        intro = Video.objects.get(intro=True)
        self.assertEqual(Video.get_intro(Video), intro)

    def test3_get_intro(self):

        """
        Testing get_intro function
        Testcase where there are more then one intro-videos
        """
        Video.objects.create(title='Test8', video='/media/videos/Intro2.mp2', era=self.sonstiges, intro=True)
        intro = list(Video.objects.filter(intro=True))
        self.assertEqual(Video.get_intro(Video), intro[0])

    def test4_get_era(self):
    
        """
        Testing get_era function
        One Video for every era, checking if they will be given back by the function
        """
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era=self.frühzeit)
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.helenismus)
        Video.objects.create(title='Test3', video='/media/videos/Test3.mp4', era=self.römisch)
        Video.objects.create(title='Test4', video='/media/videos/Test4.mp4', era=self.spätantike)
        Video.objects.create(title='Test5', video='/media/videos/Test5.mp4', era=self.klassik)
        Video.objects.create(title='Test6', video='/media/videos/Test6.mp4', era=self.archaik)

        fruehzeit = Video.objects.filter(era__name='Frühzeit')
        hellenismus = Video.objects.filter(era__name='Hellenismus')
        roemische = Video.objects.filter(era__name='Römische Kaiserzeit')
        spaet = Video.objects.filter(era__name='Spätantike')
        klassik = Video.objects.filter(era__name='Klassik')
        archaik = Video.objects.filter(era__name='Archaik')

        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list(archaik))
        self.assertEqual(list(Video.get_era(Video, 'Frühzeit')), list(fruehzeit))
        self.assertEqual(list(Video.get_era(Video, 'Hellenismus')), list(hellenismus))
        self.assertEqual(list(Video.get_era(Video, 'Römische Kaiserzeit')), list(roemische))
        self.assertEqual(list(Video.get_era(Video, 'Klassik')), list(klassik))
        self.assertEqual(list(Video.get_era(Video, 'Spätantike')), list(spaet))

    def test5__str__(self):

        """
        Tests the __str__ function
        """
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era=self.frühzeit)
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.helenismus)

        intro = Video.objects.get(title='Test1').__str__()
        test2 = Video.objects.get(title='Test2').__str__()
        self.assertEqual(intro, 'Test1')
        self.assertEqual(test2, 'Test2')


class ViewsTestCases(TestCase):
    """
    Testcases for the functions in view
    """
    def setUp(self):

        """
        Setting up objects and a client for the tests
        """
        self.client = Client()
        self.frühzeit = Era.objects.create(name='Frühzeit')
        self.archaik = Era.objects.create(name='Archaik')
        self.helenismus = Era.objects.create(name='Helenismus')
        self.römisch = Era.objects.create(name='Römische Kaiserzeit')
        self.klassik = Era.objects.create(name='Klassik')
        self.spätantike = Era.objects.create(name='Spätantike')
        self.sonstiges = Era.objects.create(name='Sonstiges')
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era=self.frühzeit)
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.helenismus)
        Video.objects.create(title='Test3', video='/media/videos/Test3.mp4', era=self.römisch)
        Video.objects.create(title='Test4', video='/media/videos/Test4.mp4', era=self.spätantike)
        Video.objects.create(title='Test5', video='/media/videos/Test5.mp4', era=self.klassik)
        Video.objects.create(title='Test6', video='/media/videos/Test6.mp4', era=self.archaik)
        Video.objects.create(title='Test5', video='/media/videos/Test5.mp4', era=self.klassik)

    def test1(self):
        """
        Testing display function in view
        """
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['Era'][self.frühzeit]), 1)
        self.assertEqual(len(response.context['Era'][self.archaik]), 1)
        self.assertEqual(len(response.context['Era'][self.helenismus]), 1)
        self.assertEqual(len(response.context['Era'][self.römisch]), 1)
        self.assertEqual(len(response.context['Era'][self.klassik]), 2)
        self.assertEqual(len(response.context['Era'][self.spätantike]), 1)
