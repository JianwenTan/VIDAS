
import platform

class python_tool:

    def __init__(self):

        pass

    #   3 ϵͳ���
    def system_pla(self):
        #   ϵͳ��Ϣ��ע
        system_info = [
            ['Linux', 'aarch64'],  # Ƕ��ʽ����
            ['Windows', 'AMD64'],  # Windows����
            ['Linux', 'X86_64']  # Linux����
        ]
        #   ��ȡϵͳID
        system_id = platform.system()
        #   ��ȡCPU��ID
        machine_id = platform.machine()
        #   �ж��Ƿ�ΪǶ��ʽ����
        if system_id == system_info[0][0] and machine_id == system_info[0][1]:
            return True
        else:
            return False