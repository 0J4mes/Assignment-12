from nytimes_api import NYTimesAPI


def display_menu():
    """Display the main menu options"""
    print("\nNYTimes API Explorer")
    print("1. Search Articles")
    print("2. Get Most Popular Articles")
    print("3. Search Movie Reviews")
    print("4. Exit")


def search_articles(api):
    """Handle article search functionality"""
    query = input("\nEnter search query (e.g. 'technology', 'politics'): ").strip()
    if not query:
        print("Error: Search query cannot be empty")
        return

    begin_date = input("Enter begin date (YYYYMMDD or leave blank): ").strip()
    params = {'query': query}
    if begin_date:
        params['begin_date'] = begin_date

    print("\nFetching articles...")
    results = api.search_articles(**params)

    if results:
        df = api.articles_to_dataframe(results)
        print(f"\nFound {len(df)} articles:")
        print(df.head())
        df.to_csv("articles.csv", index=False)
        print("\nResults saved to 'articles.csv'")


def search_movies(api):
    """Handle movie review search functionality"""
    query = input("\nEnter movie title (e.g. 'Avengers', 'Inception'): ").strip()
    if not query:
        print("Error: Movie title cannot be empty")
        return

    print("\nFetching movie reviews...")
    results = api.search_movie_reviews(query=query)

    if results:
        df = api.movies_to_dataframe(results)
        print(f"\nFound {len(df)} reviews:")
        print(df.head())
        df.to_csv("movie_reviews.csv", index=False)
        print("\nResults saved to 'movie_reviews.csv'")


def main():
    """Main program execution"""
    api = NYTimesAPI()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            search_articles(api)
        elif choice == "2":
            print("\nMost Popular feature coming soon!")
        elif choice == "3":
            search_movies(api)
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()