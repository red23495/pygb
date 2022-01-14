from pygb.motherboard import Motherboard

if __name__ == '__main__':
    try:
        motherboard = Motherboard()
        motherboard.run()
    except Exception as e:
        print("ERROR: ", str(e))

