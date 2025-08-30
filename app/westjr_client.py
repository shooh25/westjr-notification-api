import westjr
from app.const import TARGET_DIRECTIONS, TARGET_TYPES, TARGET_LINES

# 遅延が発生している列車情報を取得する
def get_delay_trains(target_line, target_direction):
    jr = westjr.WestJR(area="kinki")
    delay_trains = []
    try:
        trains = jr.get_trains(line=target_line).trains
        info = jr.get_traffic_info()
        # print(info)
        for tr in trains:
            if tr.direction == target_direction and tr.type in TARGET_TYPES:
                prev, next = jr.convert_pos(train=tr, line=target_line)
                if tr.delayMinutes >= 0:
                    delay_trains.append({
                        "prev": prev,
                        "next": next,
                        "type": tr.displayType,
                        "delay": tr.delayMinutes,
                        "dest": tr.dest.text
                    })
        return {
            "status": "success",
            "message": "遅延情報を取得しました",
            "data": delay_trains
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }

# 遅延した列車情報をもとにメッセージを生成する
def get_attention_messages(target_line, target_direction):
    if target_direction not in TARGET_DIRECTIONS or target_line not in TARGET_LINES:
        return ["無効な路線または方向です。"]
    request = get_delay_trains(target_line, target_direction)
    if request["status"] == "error":
        return [request["message"]]
    trains = request["data"]
    if len(trains) >= 1:
        messages = []
        for train in trains:
            prev = train['prev']
            next_ = train['next']
            dest = train['dest']
            train_type = train['type']
            delay = train['delay']
            if next_ is None:
                messages.append(f"{prev}停車中の{dest}行き{train_type}が{delay}分遅れ")
            else:
                messages.append(f"{prev} → {next_}間の{dest}行き{train_type}が{delay}分遅れ")
        return messages
    return ["遅延情報はありません"]

# 呼び出し例
if __name__ == "__main__":
    target_line = "kyoto"
    target_direction = 0

    messages = get_attention_messages(target_line, target_direction)
    print(messages)
