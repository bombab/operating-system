from collections import deque # collection 모듈에서 deque (double-ended queue) import

# 생성되는 준비 큐의 시간 할당량을 계산하는 데 쓰일 변수
var_pivot = 0

# 프로세스 데이터를 입력할 리스트 - (순서대로) 프로세스 id, 도착시간, 서비스시간, 현재 위치한 Ready Queue의 넘버

process_info = []

# (순서대로) 프로세스 별 남은 서비스 시간, 현재 위치한 Ready Queue에서의 남은 시간 할당량
remained_time = {}

# 생성된 준비큐
RQ_list = []

# 프로세스별 도착 시간
arrive_time = []

# 준비 큐 클래스
class Ready_Queue:        
    def __init__(self, pivot):
        self.time_quota = 2 ** pivot
        self.queue = deque([])
        
        
        

# 준비 큐 생성, 업데이트 된 RQ_list 반환
def create_RQ(var_pivot, RQ_list):
    RQ_list.append(Ready_Queue(var_pivot))
    return RQ_list 

# 필요한 준비큐가 있는지 검사
def is_RQ_exist(RQ_list, RQnum): # RQ_list, 진입해야 하는 RQ넘버링
    if len(RQ_list) -1 >= RQnum :
        return 1
    else :
        return 0
    
    
# 시간에 따른 프로세스 도착 식별
def Find_Process(process_info, time):
    PID_list = []
    
    for i in range(len(process_info)):
        if process_info[i][1] == time:
            PID_list.append(process_info[i][0])
            
    return PID_list

# 해당 시간대에 현재 모든 큐에 대하여 남아있는 프로세스 개수 반환
def remained_on_queue(RQ_list): 
    remained_num = 0

    for RQi in RQ_list:
        remained_num += len(RQi.queue)
    
    return remained_num

# 예외 생성 및 예외 문구 출력    
class PID_Error(Exception):
    def __str__(self):
        return "허용된 프로세스 ID값을 초과했습니다."

# 프로세스 ID값 초과 여부 검사
def isPID_Error(PID_num):
    if PID_num > 99:
        raise PID_Error()
    

# 프로세스 결과 값을 출력하는 함수
def print_result(process_info, PID_num, time):
    process_end = []
    
    for i in process_info:
        if i[0] == PID_num:
            process_end.append(i)
    
    for i in process_end:
        print("1. 프로세스 id : {0}, 2. 도착 시간 : {1}, 3. 서비스 시간 : {2}, 4. 종료 시간 : {3}, 5. 반환 시간 : {4}, 6. 정규화된 반환 시간 : {5:0.2f}".format(
            i[0], i[1], i[2], time, time - i[1], (time - i[1])/i[2]))

# 도착한 프로세스를 준비큐 RQ0에 올리는 작업 수행
def put_on_RQ0(process_info, time, RQ_list, var_pivot):

    arrived_process = Find_Process(process_info, time)

    for process in process_info:
        if process[0] in arrived_process:
            process[3] = 0 # 해당 프로세스의 현 RQ 위치 값을 0으로 초기화
            remained_time[process[0]][1] = 1 # 해당 프로세스의 남은 할당량을 1로 초기화
            
    if is_RQ_exist(RQ_list, 0) == 1:
            for i in range(len(arrived_process)):
                RQ_list[0].queue.appendleft(arrived_process[i])
    else :
        RQ_list = create_RQ(var_pivot, RQ_list)
        var_pivot = var_pivot + 1
        for i in range(len(arrived_process)):
            RQ_list[0].queue.appendleft(arrived_process[i])

    return process_info, RQ_list, var_pivot
    
# 스케줄링 시작
def Start_Scheduling(process_info, remained_time, var_pivot, RQ_list, arrive_time):
    # 시간 진행을 나타내는 변수, 초기값은 0
    time = 0
    while True:
        
        # 모든 프로세스가 종료된 것은 아니나 현재 큐에 올라가 있는 프로세스가 전혀 없는 경우
        if remained_on_queue(RQ_list) == 0 and len(remained_time) != 0:
            # 프로세스가 도착하였을 경우 RQ0 큐에 올리는 작업 수행
            process_info, RQ_list, var_pivot = put_on_RQ0(process_info, time, RQ_list, var_pivot)
            if len(RQ_list[0].queue) == 0:
                time = time + 1
                continue
        
        for RQi in RQ_list : # 준비큐 RQi에 대해서 살펴본다
            breaker = 0 # 2중 반복문 탈출을 위한 장치
            while True:
                # RQi의 큐가 비워져있지 않음
                if len(RQi.queue) != 0:
                    remained_time[list(RQi.queue)[-1]][0] -= 1
                    remained_time[list(RQi.queue)[-1]][1] -= 1
                    time = time + 1
                    # 새로운 프로세스가 도착
                    if time in arrive_time :
                        process_info, RQ_list, var_pivot = put_on_RQ0(process_info, time, RQ_list, var_pivot)
                    # 해당 큐의 첫번째 프로세스의 서비스시간 만료
                    if remained_time[list(RQi.queue)[-1]][0] == 0:
                        print_result(process_info, list(RQi.queue)[-1], time)
                        del remained_time[list(RQi.queue)[-1]]
                        RQi.queue.pop()
                        # 이때 프로세스가 도착해 RQ0에 올라와있을 경우 처음부터 진행
                        if len(RQ_list[0].queue) != 0:
                            breaker = 1
                            break
                        # 프로세스 서비스를 종료시킴으로서 해당 RQi에 진입해있는 프로세스가 없는 경우
                        if len(RQi.queue) == 0:
                            break
                        
                    # 모든 프로세스가 종료    
                    if len(remained_time) == 0:
                        return 0
                    # 해당 프로세스의 잔여할당량이 0 이하 이고 모든 큐에 유일하게 남아있는 프로세스가 아닐 시
                    if remained_time[list(RQi.queue)[-1]][1] <= 0 and remained_on_queue(RQ_list) != 1:
                        # 해당 프로세스를 준비큐 RQ(i+1)로 이동
                        if RQi == RQ_list[-1]: # RQ(i+1)인 준비큐가 없다면 생성후 해당 큐로 이동
                            RQ_list = create_RQ(var_pivot, RQ_list)
                            var_pivot = var_pivot + 1
                            RQ_list[-1].queue.appendleft(list(RQi.queue)[-1])
                            remained_time[list(RQi.queue)[-1]][1] = RQ_list[-1].time_quota
                            RQi.queue.pop()
                            # 이때 프로세스가 도착해 RQ0에 올라와있을 경우 처음부터 진행
                            if len(RQ_list[0].queue) != 0:
                                breaker = 1
                                break
                        else: # 이미 존재한다면 해당 큐로 바로 이동
                            RQ_list[RQ_list.index(RQi)+1].queue.appendleft(list(RQi.queue)[-1])
                            remained_time[list(RQi.queue)[-1]][1] = RQ_list[RQ_list.index(RQi)+1].time_quota
                            RQi.queue.pop()
                            # 이때 프로세스가 도착해 RQ0에 올라와있을 경우 처음부터 진행
                            if len(RQ_list[0].queue) != 0:
                                breaker = 1
                                break
                else : # RQi가 비워져있음 -> break 문을 통해 다음 RQ(i+1)로 이동
                    break
        
            if breaker == 1:
                break
            
    
    
    

# 바탕화면에 있는 input.txt파일 읽어오기
Test_File = open("C:/Users/cji/Desktop/input.txt", 'r')

text_lines = Test_File.readlines()
try:
    for line in text_lines:
        if int(line[0]) == 0:
            break
        else:
            process_data = list(map(int, line.split(',')))
            isPID_Error(process_data[0])
            process_info.append(process_data + [None])
            remained_time[process_data[0]] = [process_data[2]] + [0] 
            arrive_time.append(process_data[1])
except PID_Error as e:
    print(e)

Test_File.close()

# 스케줄링 실행
Start_Scheduling(process_info, remained_time, var_pivot, RQ_list, arrive_time)