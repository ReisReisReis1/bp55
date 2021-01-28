""""
Test for the App: video-content
"""
from django.test import Client, TestCase
from video_content.models import Video, Timestamp
from details_page.models import Era
from model_bakery import baker


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
        self.hellenismus = Era.objects.create(name='Hellenismus')
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
        self.assertEqual(list(Video.get_era(Video, 'Hellenismus')), list())
        self.assertEqual(list(Video.get_era(Video, 'Römische Kaiserzeit')), list())
        self.assertEqual(list(Video.get_era(Video, 'Klassik')), list())
        self.assertEqual(list(Video.get_era(Video, 'Spätantike')), list())
        self.assertEqual(list(Video.get_era(Video, 'Archaik')), list())

    def test2_get_intro(self):
        """
        Testing get_intro function
        Testcase where there is only one intro-video
        """
        Video.objects.create(title='Intro1', video='/media/videos/Intro.mp4', era=self.sonstiges,
                             intro=True)
        intro = Video.objects.get(intro=True)
        self.assertEqual(Video.get_intro(Video), intro)

    def test3_get_intro(self):
        """
        Testing get_intro function
        Testcase where there are more then one intro-videos
        """
        Video.objects.create(title='Test8', video='/media/videos/Intro2.mp2', era=self.sonstiges,
                             intro=True)
        intro = list(Video.objects.filter(intro=True))
        self.assertEqual(Video.get_intro(Video), intro[0])

    def test4_get_era(self):
        """
        Testing get_era function
        One Video for every era, checking if they will be given back by the function
        """
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era=self.frühzeit)
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.hellenismus)
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
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.hellenismus)

        intro = Video.objects.get(title='Test1').__str__()
        test2 = Video.objects.get(title='Test2').__str__()
        self.assertEqual(intro, 'Test1')
        self.assertEqual(test2, 'Test2')

    def test6_get_timestamps_by_video(self):
        """
        Testing the timestamp function get_timestamp_video
        No elements getting returned
        """
        self.assertEqual(list(Timestamp.get_timestamps_by_video(Timestamp, 1)), list())
        self.assertEqual(list(Timestamp.get_timestamps_by_video(Timestamp, 2)), list())

    def test7_get_timestamp_by_building(self):
        """
        Testing the timestamp function get_timestamp_by_building
        No elements getting returned
        """
        self.assertEqual(list(Timestamp.get_timestamps_by_building(Timestamp, 1)), list())
        self.assertEqual(list(Timestamp.get_timestamps_by_building(Timestamp, 2)), list())

    def test8_get_timestamp_by_video_by_building(self):
        """
        Testing the timestamp function get_timestamp_by_video
        One element getting returned
        """
        self.building1 = baker.make('details_page.Building')
        self.video1 = baker.make('video_content.Video')
        self.timestamp = Timestamp.objects.create(building=self.building1,
                                                  video=self.video1, time=5.00)
        self.assertEqual(list(Timestamp.get_timestamps_by_video(Timestamp, self.video1)),
                         [self.timestamp])

    def test9_get_timestamp_by_building(self):
        """
        Testing the timestamp function get_timestamp_by_building
        One element getting returned
        """
        self.building1 = baker.make('details_page.Building')
        self.video1 = baker.make('video_content.Video')
        self.timestamp = Timestamp.objects.create(building=self.building1,
                                                  video=self.video1, time=5.00)
        self.assertEqual(list(Timestamp.get_timestamps_by_building(Timestamp, self.building1)),
                         [self.timestamp])

    def test10_get_timestamp_by_video(self):
        """
        Testing the timestamp function get_timestamp_by_video
        Multiple elements getting returned
        """
        self.building1 = baker.make('details_page.Building')
        self.video1 = baker.make('video_content.Video')
        self.timestamp = Timestamp.objects.create(building=self.building1,
                                                  video=self.video1, time=5.00)
        self.building2 = baker.make('details_page.Building')
        self.building3 = baker.make('details_page.Building')
        self.building4 = baker.make('details_page.Building')

        self.video2 = baker.make('video_content.Video')
        self.video3 = baker.make('video_content.Video')
        self.video4 = baker.make('video_content.Video')

        self.timestamp1 = Timestamp.objects.create(building=self.building4, video=self.video3,
                                                   time=14.23)
        self.timestamp2 = Timestamp.objects.create(building=self.building2, video=self.video2,
                                                   time=0.00)
        self.timestamp3 = Timestamp.objects.create(building=self.building1, video=self.video4,
                                                   time=0.01)
        self.timestamp4 = Timestamp.objects.create(building=self.building3, video=self.video1,
                                                   time=2.45)
        self.timestamp6 = Timestamp.objects.create(building=self.building3, video=self.video3,
                                                   time=10.20)
        self.timestamp7 = Timestamp.objects.create(building=self.building2, video=self.video3,
                                                   time=10.20)
        self.timestamp8 = Timestamp.objects.create(building=self.building2, video=self.video2,
                                                   time=10.20)
        self.timestamp9 = Timestamp.objects.create(building=self.building4, video=self.video3,
                                                   time=10.20)
        self.timestamp10 = Timestamp.objects.create(building=self.building2, video=self.video4,
                                                    time=10.20)
        self.timestamp11 = Timestamp.objects.create(building=self.building3, video=self.video4,
                                                    time=10.20)

        self.assertListEqual(list(Timestamp.get_timestamps_by_video(Timestamp, self.video3)),
                             [self.timestamp1, self.timestamp6, self.timestamp7, self.timestamp9])
        self.assertListEqual(list(Timestamp.get_timestamps_by_video(Timestamp, self.video2)),
                             [self.timestamp2, self.timestamp8])
        self.assertListEqual(list(Timestamp.get_timestamps_by_video(Timestamp, self.video4)),
                             [self.timestamp3, self.timestamp10, self.timestamp11])

    def test11_get_timestamp_by_building(self):
        """
        Testing the timestamp function get_timestamp_by_building
        Multiple elements returned
        """
        self.building1 = baker.make('details_page.Building')
        self.video1 = baker.make('video_content.Video')
        self.timestamp = Timestamp.objects.create(building=self.building1,
                                                  video=self.video1, time=5.00)
        self.building2 = baker.make('details_page.Building')
        self.building3 = baker.make('details_page.Building')
        self.building4 = baker.make('details_page.Building')

        self.video2 = baker.make('video_content.Video')
        self.video3 = baker.make('video_content.Video')
        self.video4 = baker.make('video_content.Video')

        self.timestamp1 = Timestamp.objects.create(building=self.building4, video=self.video3,
                                                   time=14.23)
        self.timestamp2 = Timestamp.objects.create(building=self.building2, video=self.video2,
                                                   time=0.00)
        self.timestamp3 = Timestamp.objects.create(building=self.building1, video=self.video4,
                                                   time=0.01)
        self.timestamp4 = Timestamp.objects.create(building=self.building3, video=self.video1,
                                                   time=2.45)
        self.timestamp6 = Timestamp.objects.create(building=self.building3, video=self.video3,
                                                   time=10.20)
        self.timestamp7 = Timestamp.objects.create(building=self.building2, video=self.video3,
                                                   time=10.20)
        self.timestamp8 = Timestamp.objects.create(building=self.building2, video=self.video2,
                                                   time=10.20)
        self.timestamp9 = Timestamp.objects.create(building=self.building4, video=self.video3,
                                                   time=10.20)
        self.timestamp10 = Timestamp.objects.create(building=self.building2, video=self.video4,
                                                    time=10.20)
        self.timestamp11 = Timestamp.objects.create(building=self.building3, video=self.video4,
                                                    time=10.20)

        self.assertListEqual(list(Timestamp.get_timestamps_by_building(Timestamp, self.building2)),
                             [self.timestamp2, self.timestamp7, self.timestamp8, self.timestamp10])
        self.assertListEqual(list(Timestamp.get_timestamps_by_building(Timestamp, self.building3)),
                             [self.timestamp4, self.timestamp6, self.timestamp11])
        self.assertListEqual(list(Timestamp.get_timestamps_by_building(Timestamp, self.building4)),
                             [self.timestamp1, self.timestamp9])


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
        self.hellenismus = Era.objects.create(name='Helenismus')
        self.römisch = Era.objects.create(name='Römische Kaiserzeit')
        self.klassik = Era.objects.create(name='Klassik')
        self.spätantike = Era.objects.create(name='Spätantike')
        self.sonstiges = Era.objects.create(name='Sonstiges')
        Video.objects.create(title='Test1', video='/media/videos/Test1.mp4', era=self.frühzeit)
        Video.objects.create(title='Test2', video='/media/videos/Test2.mp4', era=self.hellenismus)
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
        self.assertEqual(len(response.context['Era'][self.hellenismus]), 1)
        self.assertEqual(len(response.context['Era'][self.römisch]), 1)
        self.assertEqual(len(response.context['Era'][self.klassik]), 2)
        self.assertEqual(len(response.context['Era'][self.spätantike]), 1)
