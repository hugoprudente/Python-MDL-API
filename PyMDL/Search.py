import bs4
import requests


class Search:
    def __init__(self):
        self.items = 0
        self.names = []

    def search(self, name: str, style: str = None, year: int = None, eps: int = None, max_results=20):
        if max_results > 20:
            print("Cannot have more than 20 Results!")
            max_results = 20
        url = f"https://mydramalist.com/search?q={name.replace(' ', '+')}"
        base = requests.get(url)
        # noinspection PyUnboundLocalVariable
        soup = bs4.BeautifulSoup(base.text, 'lxml')
        results_box = soup.find('div', class_='col-lg-8 col-md-8').find_all('div', class_='box')
        for item in results_box[:max_results]:
            # Title
            curr_title = item.find("h6").find('a').text
            curr_cateory = item.find('span', class_='text-muted').text
            filter_check = [True, True, True]  # This is to check for filters, [0] is style, [1] is year, [2] is eps

            # Check for Episodes Filter
            if eps:
                if not ((curr_cateory.split(',')[-1]).startswith(f" {eps} episode")):
                    filter_check[2] = False

            # Check for Year Filter
            if year:
                if not curr_cateory.split(',')[0].split('-')[-1].strip() == str(year):
                    filter_check[1] = False

            # Check for Style Filter
            if style:
                if curr_cateory.find(style) == -1:
                    filter_check[0] = False

            # Add it to list if checks pass
            if filter_check == [True, True, True]:
                self.names.append(curr_title)
            # Category
            # results[curr_title].append(item.find('span', class_='text-muted').text)
            # Score
            # results[curr_title].append(item.find('span', class_='score').text)
            # Description
            # results[curr_title].append(item.find_all('p')[1].text)
            self.items = len(self.names)


if __name__ == "__main__":
    res = Search()
    # print(res.items)
    res.search(input("Enter a movie or drama name to find them on the site: "))
    # res.search('Flower of evil', year=2020)
    print("Items:", res.items)
    print(res.names)
