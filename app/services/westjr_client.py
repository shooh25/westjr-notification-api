import westjr
from app.const import TARGET_DIRECTIONS, TARGET_TYPES, TARGET_LINES
from app.models.models import TrainsItem
from typing import List

jr = westjr.WestJR(area="kinki")

# 指定された路線と方向に基づき、遅延している列車を絞り込む
def filter_delay_train(train: TrainsItem, target_direction: int) -> TrainsItem | None:
    if train.direction == target_direction and train.type in TARGET_TYPES:
        if train.delayMinutes >= 0:
            return train
    return None

# 遅延が発生している列車一覧を取得する
def get_delay_trains(target_line: str, target_direction: int):
    delay_trains: List[TrainsItem] = []
    try:
        trains: List[TrainsItem] = jr.get_trains(line=target_line).trains
        for train in trains:
            result: TrainsItem | None = filter_delay_train(train, target_direction=target_direction)
            if result is not None:
                delay_trains.append(result)
        return {
            "status": "success",
            "message": "遅延情報を取得しました",
            "data": delay_trains
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

# 列車情報を元にメッセージを返す
def get_attention_messages(target_line: str, target_direction: int):
    if target_direction not in TARGET_DIRECTIONS or target_line not in TARGET_LINES:
        return ["無効な路線または方向です。"]
    
    request = get_delay_trains(target_line, target_direction)
    if request["status"] == "error":
        return [request["message"]]
    
    trains = request["data"]
    if len(trains) >= 1:
        return create_delay_messages(trains, target_line)
    return ["遅延情報はありません"]

# 遅延が発生している場合のメッセージを生成する
def create_delay_messages(trains: List[TrainsItem], target_line: str) -> List[str]:
    messages = []
    for train in trains:
        prev, next = jr.convert_pos(train=train, line=target_line)
        dest = train.dest.text if hasattr(train.dest, "text") else train.dest
        train_type = train.displayType if hasattr(train, "displayType") else train.type
        delay = train.delayMinutes
        if next is None:
            messages.append(f"{prev}停車中の{dest}行き{train_type}が{delay}分遅れ")
        else:
            messages.append(f"{prev} → {next}間の{dest}行き{train_type}が{delay}分遅れ")
    return messages

if __name__ == "__main__":
    target_line = "kyoto"
    target_direction = 0
    messages = get_attention_messages(target_line, target_direction)
    print(messages)
