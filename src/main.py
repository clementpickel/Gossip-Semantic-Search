from extract import Extract

def main():
    extract = Extract()
    data = extract.get_data_rss()
    for key in data[0]["entries"][0]:
        print(key)
    extract.save_data(data)

if __name__ == "__main__":
    main()