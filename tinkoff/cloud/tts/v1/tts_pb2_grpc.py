"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tinkoff.cloud.tts.v1 import (
    tts_pb2 as tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2,
)


class TextToSpeechStub:
    """Speech synthesis."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListVoices = channel.unary_unary(
            "/tinkoff.cloud.tts.v1.TextToSpeech/ListVoices",
            request_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesRequest.SerializeToString,
            response_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesResponses.FromString,
        )
        self.Synthesize = channel.unary_unary(
            "/tinkoff.cloud.tts.v1.TextToSpeech/Synthesize",
            request_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.SerializeToString,
            response_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechResponse.FromString,
        )
        self.StreamingSynthesize = channel.unary_stream(
            "/tinkoff.cloud.tts.v1.TextToSpeech/StreamingSynthesize",
            request_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.SerializeToString,
            response_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.StreamingSynthesizeSpeechResponse.FromString,
        )


class TextToSpeechServicer:
    """Speech synthesis."""

    @staticmethod
    def ListVoices(request, context):
        """Method for retrieving available voices list."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    @staticmethod
    def Synthesize(request, context):
        """Method for the non-streaming synthesis."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    @staticmethod
    def StreamingSynthesize(request, context):
        """Method for streaming synthesis."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TextToSpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListVoices": grpc.unary_unary_rpc_method_handler(
            servicer.ListVoices,
            request_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesRequest.FromString,
            response_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesResponses.SerializeToString,
        ),
        "Synthesize": grpc.unary_unary_rpc_method_handler(
            servicer.Synthesize,
            request_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.FromString,
            response_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechResponse.SerializeToString,
        ),
        "StreamingSynthesize": grpc.unary_stream_rpc_method_handler(
            servicer.StreamingSynthesize,
            request_deserializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.FromString,
            response_serializer=tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.StreamingSynthesizeSpeechResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "tinkoff.cloud.tts.v1.TextToSpeech", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class TextToSpeech:
    """Speech synthesis."""

    @staticmethod
    def ListVoices(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/tinkoff.cloud.tts.v1.TextToSpeech/ListVoices",
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesRequest.SerializeToString,
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.ListVoicesResponses.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Synthesize(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/tinkoff.cloud.tts.v1.TextToSpeech/Synthesize",
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.SerializeToString,
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def StreamingSynthesize(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/tinkoff.cloud.tts.v1.TextToSpeech/StreamingSynthesize",
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.SynthesizeSpeechRequest.SerializeToString,
            tinkoff_dot_cloud_dot_tts_dot_v1_dot_tts__pb2.StreamingSynthesizeSpeechResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
