from pygb.motherboard import Motherboard

if __name__ == '__main__':
    motherboard = Motherboard()
    try:
        motherboard.run()
    except Exception as e:
        print("ERROR: ", str(e))
    finally:
        motherboard.close()

