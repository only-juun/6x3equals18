#-*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
import time


def lock_open(pin):
    print("open")
    GPIO.output(pin, True)

def lock_close(pin):
    GPIO.output(pin, False)
    print("close")
    
lock_pin = 16
GPIO.cleanup(lock_pin)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(lock_pin, GPIO.OUT)

cred = credentials.Certificate("./barcodedb-efafb-firebase-adminsdk-wujo4-01ed441f25.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
barcode_ref = db.collection(u'bigbox')



door_open = False
invalid_access = 0

docs = barcode_ref.stream()
print(docs)
for doc in docs:
  print(u'{} => {}'.format(doc.id, doc.to_dict()))


while(1):
  scan_result = input("Barcode scaner module: ")
  # ���ڵ� ��ĵ ������ DB�� �ִ��� Ȯ���ؼ� �ִ��� ������ �˰Ե�
  # ��ȿ ���ڵ�(�����, �����)�� ��� door_open = True
  # ��ȿ���ڵ尡 �ƴ� ���, invalid_access++ 
  query_ref = barcode_ref.where(u'code' , u'==',scan_result).get()      # Type: List
  # print(query_ref.id) ��� �Ұ�
  if len(query_ref)==0:        # ���ڵ尡 ����Ǿ����� ���� ���
    door_open = False
    print("invalid barcode")
    invalid_access = invalid_access+1
  else:
    doc = query_ref[0]
    valid_barcode_document = doc.id
    door_open = True
    
    lock_open(lock_pin)
    time.sleep(5)
    
    # �α�(open) �߰� �ڵ� ����
    
    lock_close(lock_pin)
    time.sleep(3)
    
    # �α�(close) �߰� �ڵ� ����
    
    door_open = False 
    
  if invalid_access > 2:
    print("Send info to App")
    # ���ø����̼����� �˸� ���� �ڵ� �ۼ�
    invalid_access = 0         # �ʱ�ȭ  
      
    
     
    
# ������ �߰�: �̿� 
#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({
#    u'first': u'Ada',
#    u'last': u'Lovelace',
#    u'born': 1815
#})
