import fs.memoryfs
import unittest
from iris_doc.api_tagger import ApiTagger, TagBuilder
from iris_doc.oc.api_tagger_oc import ObjCTagBuilder
input_output_pairs_desc = ["Delegate + Interface with tags","RTC Delegate", "Protocol with annotations and functions", "NS_SWIFT_NAME First",
    "Basic Class", "Enums", "class interfaces and complex method params",
    "Protocols", "Class import, interface properties", "Interface methods with no params, and multi params"
]
input_output_pairs = [("""@class AgoraRtcEngineKit;
@class AgoraMediaRecorder;

@protocol AgoraRtcEngineDelegate <NSObject>
@optional

#pragma mark Delegate Methods

#pragma mark Core Delegate Methods

- (void)rtcEngine:(AgoraRtcEngineKit * _Nonnull)engine firstRemoteVideoFrameOfUid:(NSUInteger)uid size:(CGSize)size elapsed:(NSInteger)elapsed NS_SWIFT_NAME(rtcEngine(_:firstRemoteVideoFrameOfUid:size:elapsed:));

@end

@interface AgoraRtcEngineKit : NSObject
@end""", """@class AgoraRtcEngineKit;
@class AgoraMediaRecorder;

/* class_agorartcenginedelegate */
@protocol AgoraRtcEngineDelegate <NSObject>
@optional

#pragma mark Delegate Methods

#pragma mark Core Delegate Methods

/* api_agorartcenginedelegate_firstremotevideoframeofuid##engine#uid#size#elapsed */
- (void)rtcEngine:(AgoraRtcEngineKit * _Nonnull)engine firstRemoteVideoFrameOfUid:(NSUInteger)uid size:(CGSize)size elapsed:(NSInteger)elapsed NS_SWIFT_NAME(rtcEngine(_:firstRemoteVideoFrameOfUid:size:elapsed:));

@end

/* class_agorartcenginekit */
@interface AgoraRtcEngineKit : NSObject
@end"""),("""@protocol AgoraRtcEngineDelegate <NSObject>
@optional

#pragma mark Delegate Methods

#pragma mark Core Delegate Methods

- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didOccurError:(AgoraErrorCode)errorCode
    NS_SWIFT_NAME(rtcEngine(_:didOccurError:));

- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    connectionChangedToState:(AgoraConnectionState)state
                      reason:(AgoraConnectionChangedReason)reason
    NS_SWIFT_NAME(rtcEngine(_:connectionChangedTo:reason:));

- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didClientRoleChanged:(AgoraClientRole)oldRole
                 newRole:(AgoraClientRole)newRole
          newRoleOptions:(AgoraClientRoleOptions *_Nullable)newRoleOptions
    NS_SWIFT_NAME(rtcEngine(_:didClientRoleChanged:newRole:newRoleOptions:));

- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
     wlAccMessage:(AgoraWlAccReason)reason
           action:(AgoraWlAccAction)action
         wlAccMsg:(NSString *_Nonnull)wlAccMsg
    NS_SWIFT_NAME(rtcEngine(_:wlAccMessage:action:wlAccMsg:));

@end""", """/* class_agorartcenginedelegate */
@protocol AgoraRtcEngineDelegate <NSObject>
@optional

#pragma mark Delegate Methods

#pragma mark Core Delegate Methods

/* api_agorartcenginedelegate_didoccurerror##engine#errorcode */
- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didOccurError:(AgoraErrorCode)errorCode
    NS_SWIFT_NAME(rtcEngine(_:didOccurError:));

/* api_agorartcenginedelegate_connectionchangedtostate##engine#state#reason */
- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    connectionChangedToState:(AgoraConnectionState)state
                      reason:(AgoraConnectionChangedReason)reason
    NS_SWIFT_NAME(rtcEngine(_:connectionChangedTo:reason:));

/* api_agorartcenginedelegate_didclientrolechanged##engine#oldrole#newrole#newroleoptions */
- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didClientRoleChanged:(AgoraClientRole)oldRole
                 newRole:(AgoraClientRole)newRole
          newRoleOptions:(AgoraClientRoleOptions *_Nullable)newRoleOptions
    NS_SWIFT_NAME(rtcEngine(_:didClientRoleChanged:newRole:newRoleOptions:));

/* api_agorartcenginedelegate_wlaccmessage##engine#reason#action#wlaccmsg */
- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
     wlAccMessage:(AgoraWlAccReason)reason
           action:(AgoraWlAccAction)action
         wlAccMsg:(NSString *_Nonnull)wlAccMsg
    NS_SWIFT_NAME(rtcEngine(_:wlAccMessage:action:wlAccMsg:));

@end"""),
("""@protocol AgoraRtmClientDelegate <NSObject>
@optional

- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onMessageEvent:(AgoraRtmMessageEvent * _Nonnull)event;

- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onPresenceEvent:(AgoraRtmPresenceEvent * _Nonnull)event;

- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onUser:(NSString * _Nonnull)userId
    joinChannel:(NSString * _Nonnull)channelName
    result:(AgoraRtmStreamChannelErrorCode)errorCode;
@end""", """/* class_agorartmclientdelegate */
@protocol AgoraRtmClientDelegate <NSObject>
@optional

/* api_agorartmclientdelegate_rtmkit##rtmkit#event */
- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onMessageEvent:(AgoraRtmMessageEvent * _Nonnull)event;

/* api_agorartmclientdelegate_rtmkit##rtmkit#event */
- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onPresenceEvent:(AgoraRtmPresenceEvent * _Nonnull)event;

/* api_agorartmclientdelegate_rtmkit##rtmkit#userid#channelname#errorcode */
- (void)rtmKit:(AgoraRtmClientKit * _Nonnull)rtmKit
    onUser:(NSString * _Nonnull)userId
    joinChannel:(NSString * _Nonnull)channelName
    result:(AgoraRtmStreamChannelErrorCode)errorCode;
@end"""),
("""NS_SWIFT_NAME(AgoraVideoRenderingTracingInfo) __attribute__((visibility("default"))) @interface AgoraVideoRenderingTracingInfo : NSObject
@property (assign, nonatomic)
    NSInteger elapsedTime NS_SWIFT_NAME(elapsedTime);
@property (assign, nonatomic) NSInteger start2JoinChannel NS_SWIFT_NAME(start2JoinChannel);
@property (assign, nonatomic) NSInteger join2JoinSuccess NS_SWIFT_NAME(join2JoinSuccess);
@property (assign, nonatomic) NSInteger joinSuccess2RemoteJoined NS_SWIFT_NAME(joinSuccess2RemoteJoined);
@property (assign, nonatomic) NSInteger remoteJoined2SetView NS_SWIFT_NAME(remoteJoined2SetView);
@property (assign, nonatomic) NSInteger remoteJoined2UnmuteVideo NS_SWIFT_NAME(remoteJoined2UnmuteVideo);
@property (assign, nonatomic) NSInteger remoteJoined2PacketReceived NS_SWIFT_NAME(remoteJoined2PacketReceived);

@end""","""/* class_agoravideorenderingtracinginfo */
NS_SWIFT_NAME(AgoraVideoRenderingTracingInfo) __attribute__((visibility("default"))) @interface AgoraVideoRenderingTracingInfo : NSObject
/* class_agoravideorenderingtracinginfo_elapsedtime */
@property (assign, nonatomic)
    NSInteger elapsedTime NS_SWIFT_NAME(elapsedTime);
/* class_agoravideorenderingtracinginfo_start2joinchannel */
@property (assign, nonatomic) NSInteger start2JoinChannel NS_SWIFT_NAME(start2JoinChannel);
/* class_agoravideorenderingtracinginfo_join2joinsuccess */
@property (assign, nonatomic) NSInteger join2JoinSuccess NS_SWIFT_NAME(join2JoinSuccess);
/* class_agoravideorenderingtracinginfo_joinsuccess2remotejoined */
@property (assign, nonatomic) NSInteger joinSuccess2RemoteJoined NS_SWIFT_NAME(joinSuccess2RemoteJoined);
/* class_agoravideorenderingtracinginfo_remotejoined2setview */
@property (assign, nonatomic) NSInteger remoteJoined2SetView NS_SWIFT_NAME(remoteJoined2SetView);
/* class_agoravideorenderingtracinginfo_remotejoined2unmutevideo */
@property (assign, nonatomic) NSInteger remoteJoined2UnmuteVideo NS_SWIFT_NAME(remoteJoined2UnmuteVideo);
/* class_agoravideorenderingtracinginfo_remotejoined2packetreceived */
@property (assign, nonatomic) NSInteger remoteJoined2PacketReceived NS_SWIFT_NAME(remoteJoined2PacketReceived);

@end"""),
("""@interface AgoraRtcEngineKit
- (int)enableDualStreamMode:(BOOL)enabled
    streamConfig:(AgoraSimulcastStreamConfig* _Nonnull)streamConfig NS_SWIFT_NAME(enableDualStreamMode(_:streamConfig:));
@end""","""/* class_agorartcenginekit */
@interface AgoraRtcEngineKit
/* api_agorartcenginekit_enabledualstreammode##enabled#streamconfig */
- (int)enableDualStreamMode:(BOOL)enabled
    streamConfig:(AgoraSimulcastStreamConfig* _Nonnull)streamConfig NS_SWIFT_NAME(enableDualStreamMode(_:streamConfig:));
@end"""),
("""/** Audience latency levels in broadcaster mode. */
typedef NS_ENUM(NSInteger, AgoraAudienceLatencyLevelType) {
    /** 1: Low latency. A low latency audience's jitter buffer is 1.2 second. */
    AgoraAudienceLatencyLevelLowLatency = 1,
    /** 2: Default Ultra low latency. An ultra low latency audience's jitter buffer is 0.5 second. */
    AgoraAudienceLatencyLevelUltraLowLatency = 2,
};""","""/* enum_agoraaudiencelatencyleveltype */
typedef NS_ENUM(NSInteger, AgoraAudienceLatencyLevelType) {
/* enum_agoraaudiencelatencyleveltype_agoraaudiencelatencylevellowlatency */
    AgoraAudienceLatencyLevelLowLatency = 1,
/* enum_agoraaudiencelatencyleveltype_agoraaudiencelatencylevelultralowlatency */
    AgoraAudienceLatencyLevelUltraLowLatency = 2,
};"""),
("""NS_ASSUME_NONNULL_BEGIN
@interface AgoraRtcEngineKit(Ex)
- (int)joinChannelExByToken:(NSString* _Nullable)token
                 connection:(AgoraRtcConnection * _Nonnull)connection
                   delegate:(id<AgoraRtcEngineDelegate> _Nullable)delegate
               mediaOptions:(AgoraRtcChannelMediaOptions* _Nonnull)mediaOptions
                joinSuccess:(void(^ _Nullable)(NSString* _Nonnull channel, NSUInteger uid, NSInteger elapsed))joinSuccessBlock NS_SWIFT_NAME(joinChannelEx(byToken:connection:delegate:mediaOptions:joinSuccess:));
@end""", """/* extension_agorartcenginekit(ex) */
NS_ASSUME_NONNULL_BEGIN
@interface AgoraRtcEngineKit(Ex)
/* api_agorartcenginekit(ex)_joinchannelexbytoken##token#connection#delegate#mediaoptions#joinsuccessblock */
- (int)joinChannelExByToken:(NSString* _Nullable)token
                 connection:(AgoraRtcConnection * _Nonnull)connection
                   delegate:(id<AgoraRtcEngineDelegate> _Nullable)delegate
               mediaOptions:(AgoraRtcChannelMediaOptions* _Nonnull)mediaOptions
                joinSuccess:(void(^ _Nullable)(NSString* _Nonnull channel, NSUInteger uid, NSInteger elapsed))joinSuccessBlock NS_SWIFT_NAME(joinChannelEx(byToken:connection:delegate:mediaOptions:joinSuccess:));
@end"""),
("""NS_ASSUME_NONNULL_BEGIN
@protocol AgoraRtcMediaPlayerProtocol <NSObject>
- (int)getMediaPlayerId NS_SWIFT_NAME(getMediaPlayerId());
/**
 * Opens a media file with a specified URL.
 * @param url The URL of the media file that you want to play.
 * @return
 * - 0: Success.
 * - < 0: Failure.
 */
- (int)open:(NSString *)url startPos:(NSInteger)startPos NS_SWIFT_NAME(open(_:startPos:));
@end""", """/* class_agorartcmediaplayerprotocol */
NS_ASSUME_NONNULL_BEGIN
@protocol AgoraRtcMediaPlayerProtocol <NSObject>
/* api_agorartcmediaplayerprotocol_getmediaplayerid */
- (int)getMediaPlayerId NS_SWIFT_NAME(getMediaPlayerId());
/* api_agorartcmediaplayerprotocol_open##url#startpos */
- (int)open:(NSString *)url startPos:(NSInteger)startPos NS_SWIFT_NAME(open(_:startPos:));
@end"""),
("""@class AgoraRtcEngineKit;
__attribute__((visibility("default"))) @interface AgoraMusicContentCenterConfig : NSObject
@property(assign, nonatomic) AgoraRtcEngineKit* _Nullable rtcEngine;
/**
 * The app ID of the project that has enabled the music content center
 */
@property (nonatomic, copy) NSString *appId;
/**
 * The max number which the music content center caches cannot exceed 50.
 */
@property (nonatomic, assign) NSUInteger maxCacheSize;
@end""", """@class AgoraRtcEngineKit;
/* class_agoramusiccontentcenterconfig */
__attribute__((visibility("default"))) @interface AgoraMusicContentCenterConfig : NSObject
/* class_agoramusiccontentcenterconfig_rtcengine */
@property(assign, nonatomic) AgoraRtcEngineKit* _Nullable rtcEngine;
/* class_agoramusiccontentcenterconfig_appid */
@property (nonatomic, copy) NSString *appId;
/* class_agoramusiccontentcenterconfig_maxcachesize */
@property (nonatomic, assign) NSUInteger maxCacheSize;
@end"""),
("""/**
*  hello
*/
__attribute__((visibility("default"))) @interface AgoraLocalSpatialAudioKit : AgoraBaseSpatialAudioKit
+ (instancetype _Nonnull)sharedLocalSpatialAudioWithConfig:(AgoraLocalSpatialAudioConfig* _Nonnull)config NS_SWIFT_NAME(sharedLocalSpatialAudio(with:));
+ (void)destroy NS_SWIFT_NAME(destroy());
- (int)updateRemotePositionEx:(NSUInteger)uid positionInfo:(AgoraRemoteVoicePositionInfo* _Nonnull)posInfo connection:(AgoraRtcConnection * _Nonnull)connection NS_SWIFT_NAME(updateRemotePositionEx(_:positionInfo:connection:));
- (int)removeRemotePosition:(NSUInteger)uid NS_SWIFT_NAME(removeRemotePosition(_:));
- (int)setRemoteAudioAttenuation:(double)attenuation userId:(NSUInteger)uid forceSet:(BOOL)forceSet NS_SWIFT_NAME(setRemoteAudioAttenuation(_:userId:forceSet:));
@end""", """/* class_agoralocalspatialaudiokit */
__attribute__((visibility("default"))) @interface AgoraLocalSpatialAudioKit : AgoraBaseSpatialAudioKit
/* api_agoralocalspatialaudiokit_sharedlocalspatialaudiowithconfig##config */
+ (instancetype _Nonnull)sharedLocalSpatialAudioWithConfig:(AgoraLocalSpatialAudioConfig* _Nonnull)config NS_SWIFT_NAME(sharedLocalSpatialAudio(with:));
/* api_agoralocalspatialaudiokit_destroy */
+ (void)destroy NS_SWIFT_NAME(destroy());
/* api_agoralocalspatialaudiokit_updateremotepositionex##uid#posinfo#connection */
- (int)updateRemotePositionEx:(NSUInteger)uid positionInfo:(AgoraRemoteVoicePositionInfo* _Nonnull)posInfo connection:(AgoraRtcConnection * _Nonnull)connection NS_SWIFT_NAME(updateRemotePositionEx(_:positionInfo:connection:));
/* api_agoralocalspatialaudiokit_removeremoteposition##uid */
- (int)removeRemotePosition:(NSUInteger)uid NS_SWIFT_NAME(removeRemotePosition(_:));
/* api_agoralocalspatialaudiokit_setremoteaudioattenuation##attenuation#uid#forceset */
- (int)setRemoteAudioAttenuation:(double)attenuation userId:(NSUInteger)uid forceSet:(BOOL)forceSet NS_SWIFT_NAME(setRemoteAudioAttenuation(_:userId:forceSet:));
@end""")
]

class TestApiTaggerOc(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS
    __apiTagger: ApiTagger

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()
        self.__apiTagger = ApiTagger(
            self.__fileSystem, ObjCTagBuilder())

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def test_matchMultiple(self):
        for i, test in enumerate(input_output_pairs):
            print(f'ObjC Testing: {input_output_pairs_desc[i]}')
            path = f"member_property_{i}.h"

            self.__fileSystem.create(path, wipe=True)
            file = self.__fileSystem.open(path, mode="w")
            file.write(test[0])
            file.flush()
            file.close()
            self.__apiTagger.process(path)

            expectedContent = test[1]
            processedContent = self.__fileSystem.readtext(path)
            self.assertEqual(processedContent, expectedContent)

if __name__ == '__main__':
    unittest.main()
