import glob
import pymongo
import pickle

files = glob.glob('*.db')

def migration():
