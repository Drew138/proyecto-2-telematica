.PHONY: proto


proto:
	@python -m grpc_tools.protoc -I ./protobuf --python_out=./orchestrator/src/protobuf --pyi_out=./orchestrator/src/protobuf --grpc_python_out=./orchestrator/src/protobuf ./protobuf/register.proto
	@python -m grpc_tools.protoc -I ./protobuf --python_out=./orchestrator/src/protobuf --pyi_out=./orchestrator/src/protobuf --grpc_python_out=./orchestrator/src/protobuf ./protobuf/monitor.proto
	@python -m grpc_tools.protoc -I ./protobuf --python_out=./instance/src/protobuf --pyi_out=./instance/src/protobuf --grpc_python_out=./instance/src/protobuf ./protobuf/monitor.proto
	@python -m grpc_tools.protoc -I ./protobuf --python_out=./instance/src/protobuf --pyi_out=./instance/src/protobuf --grpc_python_out=./instance/src/protobuf ./protobuf/register.proto
