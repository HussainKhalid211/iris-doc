from iris_doc.c_sharp.api_tagger_c_sharp import CSharpTagBuilder
from iris_doc.api_tagger import ApiTagger, TagBuilder
import unittest
import fs.memoryfs


class TestApiTaggerCSharp(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS
    __apiTagger: ApiTagger

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()
        self.__apiTagger = ApiTagger(
            self.__fileSystem, CSharpTagBuilder())

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def test_matchMemberFunction(self):
        path = "member_function.cs"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
namespace Agora.Rtc
{
    ///
    /// <summary>
    /// The basic interface of the Agora SDK that implements the core functions of real-time communication.
    /// IRtcEngine provides the main methods that your app can call.Before calling other APIs, you must call CreateAgoraRtcEngine to create an IRtcEngine object.
    /// </summary>
    ///
    public abstract class IRtcEngine
    {
      public abstract int SetChannelProfile(CHANNEL_PROFILE_TYPE profile);

      public string appId { set; get; }

      public UInt64 context { set; get; }

      public int age;

      public Optional<THREAD_PRIORITY_TYPE> threadPriority = new Optional<THREAD_PRIORITY_TYPE>();
    }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
namespace Agora.Rtc
{
/* class_irtcengine */
    public abstract class IRtcEngine
    {
/* api_irtcengine_setchannelprofile */
      public abstract int SetChannelProfile(CHANNEL_PROFILE_TYPE profile);

/* class_irtcengine_appid */
      public string appId { set; get; }

/* class_irtcengine_context */
      public UInt64 context { set; get; }

/* class_irtcengine_age */
      public int age;

/* class_irtcengine_threadpriority */
      public Optional<THREAD_PRIORITY_TYPE> threadPriority = new Optional<THREAD_PRIORITY_TYPE>();
    }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        print("xiayangqun: " + processedContent)
        print("xiayangqun expected: " + expectedContent)
        self.assertEqual(processedContent, expectedContent)

    def test_matchMemberVariables(self):
        path = "member_variables.cs"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
namespace Agora.Rtc
{
  public class RtcEngineContext : OptionalJsonParse
  {
    public string appId { set; get; }
    public UInt64 context { set; get; }
    public int age;
    public Optional<THREAD_PRIORITY_TYPE> threadPriority = new Optional<THREAD_PRIORITY_TYPE>();
  }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
namespace Agora.Rtc
{
/* class_rtcenginecontext */
  public class RtcEngineContext : OptionalJsonParse
  {
/* class_rtcenginecontext_appid */
    public string appId { set; get; }
/* class_rtcenginecontext_context */
    public UInt64 context { set; get; }
/* class_rtcenginecontext_age */
    public int age;
/* class_rtcenginecontext_threadpriority */
    public Optional<THREAD_PRIORITY_TYPE> threadPriority = new Optional<THREAD_PRIORITY_TYPE>();
  }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClass(self):
        path = "match_cass.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
namespace Agora.Rtc
{
  public abstract class IMediaPlayer
  {
  }

  public abstract class IMusicPlayer : IMediaPlayer
  {
  }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
namespace Agora.Rtc
{
/* class_imediaplayer */
  public abstract class IMediaPlayer
  {
  }

/* class_imusicplayer */
  public abstract class IMusicPlayer : IMediaPlayer
  {
  }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchEnum(self):
        path = "match_enum.cs"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
    ///
    /// <summary>
    /// The status of the last-mile probe test.
    /// </summary>
    ///
    public enum LASTMILE_PROBE_RESULT_STATE
    {
        ///
        /// <summary>
        /// 1: The last-mile network probe test is complete.
        /// </summary>
        ///
        LASTMILE_PROBE_RESULT_COMPLETE = 1,

        ///
        /// <summary>
        /// 2: The last-mile network probe test is incomplete because the bandwidth estimation is not available due to limited test resources. One possible reason is that testing resources are temporarily limited.
        /// </summary>
        ///
        LASTMILE_PROBE_RESULT_INCOMPLETE_NO_BWE = 2,

        ///
        /// <summary>
        /// 3: The last-mile network probe test is not carried out. Probably due to poor network conditions.
        /// </summary>
        ///
        LASTMILE_PROBE_RESULT_UNAVAILABLE = 3
    };
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* enum_lastmile_probe_result_state */
    public enum LASTMILE_PROBE_RESULT_STATE
    {
/* enum_lastmile_probe_result_state_lastmile_probe_result_complete */
        LASTMILE_PROBE_RESULT_COMPLETE = 1,

/* enum_lastmile_probe_result_state_lastmile_probe_result_incomplete_no_bwe */
        LASTMILE_PROBE_RESULT_INCOMPLETE_NO_BWE = 2,

/* enum_lastmile_probe_result_state_lastmile_probe_result_unavailable */
        LASTMILE_PROBE_RESULT_UNAVAILABLE = 3
    };
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)


if __name__ == '__main__':
    unittest.main()
