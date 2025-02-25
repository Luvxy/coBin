# 다양한 upbit 관련 기능을 가지고 있는 functions 클래스
class functions:
    # 싱글톤 패턴으로 객체 생성
    _instance = None  # 싱글톤 인스턴스를 저장할 클래스 변수

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # 인스턴스가 없으면 새로 생성
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance  # 기존 인스턴스 반환
        
    def __init__(self, upbit):
        # 업비트 객체 생성
        self.upbit = upbit
        # 거래 코인
        self.target = []
        # 제외 코인
        self.excluded_tickers = []
    
    