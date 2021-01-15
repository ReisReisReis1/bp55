""""
Test for the App: video-content
"""
from django.test import Client
from django.test import TestCase
from video_content.models import Video

"""
class VideoTestCases(TestCase):
    def test1_get_intro_era(self):
        """"""
        Testing get_intro  and get_era function
        Testcase where there is no video
        """"""
        self.assertEqual(Video.get_intro(Video), Video.DoesNotExist)
        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list())
        self.assertEqual(list(Video.get_era(Video, 'Frühzeit')), list())
        self.assertEqual(list(Video.get_era(Video, 'Hellenismus')), list())
        self.assertEqual(list(Video.get_era(Video, 'Römische Kaiserzeit')), list())
        self.assertEqual(list(Video.get_era(Video, 'Klassik')), list())
        self.assertEqual(list(Video.get_era(Video, 'Spätantike')), list())
        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list())

    def test2_get_intro(self):

        """"""
        Testing get_intro function
        Testcase where there is only one intro-video
        """"""
        Video.objects.create(title='Intro1', video='/media/videos/Intro.mp4', era='Sonstiges', intro=True)
        intro = Video.objects.get(intro=True)
        self.assertEqual(Video.get_intro(Video), intro)

    def test3_get_intro(self):
        """"""
        Testing get_intro function
        Testcase where there are more then one intro-videos
        """"""
        Video.objects.create(title='Test8', video='/media/videos/Intro2.mp2', era='Sonstiges', intro=True)
        intro = list(Video.objects.filter(intro=True))
        self.assertEqual(Video.get_intro(Video), intro[0])

    def test4_get_era(self):
        """"""
        Testing get_era function
        One Video for every era, checking if they will be given back by the function
        """"""
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era='Frühzeit')
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era='Hellenismus')
        Video.objects.create(title='Test3', video='/media/videos/Test3.mp4', era='Römische Kaiserzeit')
        Video.objects.create(title='Test4', video='/media/videos/Test4.mp4', era='Spätantike')
        Video.objects.create(title='Test5', video='/media/videos/Test5.mp4', era='Klassik')
        Video.objects.create(title='Test6', video='/media/videos/Test6.mp4', era='Archaik')

        fruehzeit = Video.objects.filter(era='Frühzeit')
        hellenismus = Video.objects.filter(era='Hellenismus')
        roemische = Video.objects.filter(era='Römische Kaiserzeit')
        spaet = Video.objects.filter(era='Spätantike')
        klassik = Video.objects.filter(era='Klassik')
        archaik = Video.objects.filter(era='Archaik')

        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list(archaik))
        self.assertEqual(list(Video.get_era(Video, 'Frühzeit')), list(fruehzeit))
        self.assertEqual(list(Video.get_era(Video, 'Hellenismus')), list(hellenismus))
        self.assertEqual(list(Video.get_era(Video, 'Römische Kaiserzeit')), list(roemische))
        self.assertEqual(list(Video.get_era(Video, 'Klassik')), list(klassik))
        self.assertEqual(list(Video.get_era(Video, 'Spätantike')), list(spaet))

    def test5__str__(self):
        """"""
        Tests the __str__ function
        """"""
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era='Frühzeit')
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era='Hellenismus')

        intro = Video.objects.get(title='Test1').__str__()
        test2 = Video.objects.get(title='Test2').__str__()
        self.assertEqual(intro, 'Test1')
        self.assertEqual(test2, 'Test2')


class ViewsTestCases(TestCase):
    def setUp(self):
        """"""
        Setting up objects and a client for the tests
        """"""
        self.client = Client()
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era='Spätantike')
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era='Archaik')
        Video.objects.create(title='Test3', video='/media/videos/Test3.mp4', era='Frühzeit')
        Video.objects.create(title='Test4', video='/media/videos/Test4.mp4', era='Hellenismus')
        Video.objects.create(title='Test5', video='/media/videos/Test5.mp4', era='Klassik')
        Video.objects.create(title='Test6', video='/media/videos/Test6.mp4', era='Römische Kaiserzeit')
        Video.objects.create(title='Test7', video='/media/videos/Test7.mp4', era='Klassik')

    def test1(self):
        """"""
        Testing display function in view
        """"""
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['Spätantike']), 1)
        self.assertEqual(len(response.context['Archaik']), 1)
        self.assertEqual(len(response.context['Frühzeit']), 1)
        self.assertEqual(len(response.context['Hellenismus']), 1)
        self.assertEqual(len(response.context['Klassik']), 2)
        self.assertEqual(len(response.context['RömischeKaiserzeit']), 1)
"""

