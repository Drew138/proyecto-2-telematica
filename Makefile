.PHONY: proto


proto:
	@protoc --python_out=./orchestrator/src/ ./protobuf/monitor.proto
	@protoc --python_out=./node/src/ ./protobuf/monitor.proto
