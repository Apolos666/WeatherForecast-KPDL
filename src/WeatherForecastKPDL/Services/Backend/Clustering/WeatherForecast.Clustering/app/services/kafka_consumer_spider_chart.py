from kafka import KafkaConsumer
import json
from app.core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_SPIDER_CHART_CONSUMER_GROUP_ID, KAFKA_TOPIC
from app.services.clustering_service import process_and_send_data
from datetime import datetime
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_kafka_consumer(topic, group_id):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=False,  
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

async def consume_spider_chart_data():
    logging.info("Bắt đầu tiêu thụ dữ liệu từ Kafka")
    consumer = create_kafka_consumer(KAFKA_TOPIC, KAFKA_SPIDER_CHART_CONSUMER_GROUP_ID)
    data = []
    first_message_received = False
    current_year = None
    try:
        while True:
            messages = consumer.poll(timeout_ms=5000, max_records=10000)
            if not messages:
                logging.info("Không còn message nào nữa, dừng tiêu thụ dữ liệu")
                break

            for tp, msgs in messages.items():
                for msg in msgs:
                    try:
                        value = msg.value
                        if value['payload']['after'] is not None:
                            data_point = value['payload']['after']
                            time_str = data_point['Time']
                            time = datetime.fromisoformat(time_str)
                            
                            # Xác định current_year cho lần đầu tiên
                            if not first_message_received:
                                current_year = time.year
                                first_message_received = True
                            
                            data.append(data_point)
                            
                            if time.year != current_year:
                                logging.info(f"Đã chuyển sang năm mới: {time.year}, dừng tiêu thụ dữ liệu")
                                break
                    except Exception as e:
                        logging.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                        continue

            if not first_message_received:
                continue

            if time.year != current_year:
                break

        await process_and_send_data(data)
        consumer.commit()  
        logging.info("Đã xử lý và gửi dữ liệu thành công")
    except KeyboardInterrupt:
        logging.info("Tiếp nhận KeyboardInterrupt, dừng tiêu thụ dữ liệu")
    except Exception as e:
        logging.error(f"Lỗi khi tiêu thụ dữ liệu: {e}")
    finally:
        consumer.close()
        logging.info("Đã đóng kết nối Kafka")