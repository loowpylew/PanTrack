from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

YOUR_CLARIFAI_API_KEY = "1f4072bde4c84b4b8c13b36d8bb48fd1"
YOUR_APPLICATION_ID = "ID-1"
FRAME_LOCATION = "C:\\Users\\lewis\\OneDrive\\Documents\\Image_classification_for_UCL\\test_images\\rat_color.jpg"

# This is how you authenticate.
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

with open(FRAME_LOCATION, "rb") as f:
    file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="general-image-recognition",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                    )
                )
            )
        ]
    ),
    metadata=metadata
)

if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    raise Exception("Post model outputs failed, status: " + 
    post_model_outputs_response.status.description)

# Since we have one input, one output will exist here.
output = post_model_outputs_response.outputs[0]

print("Predicted concepts:")
for concept in output.data.concepts:
    """if concept.name == "animal" and concept.value >= 0.70: 
        print("Animal is in video")
    elif concept.name == "animal" and concept.value <= 0.70:
        print("None")
    elif concept.name == "mammal" and concept.value >= 0.70:
        print("Animal is in video")"""
    print("%s %.2f" % (concept.name, concept.value))