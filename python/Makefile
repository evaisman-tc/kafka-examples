
user_pb2.py: ./schemas/user.proto
	protoc -I=./schemas/ --python_out=./ ./schemas/user.proto;

clean:
	rm -f $(TARGET_DIR)/*_pb2.py