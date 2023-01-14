from database import server
from stats import reindex

def main():
    reindex.Reindex()
    query = "EXECUTE contabyx.analyze_all"
    cursor = server.New().cursor
    cursor.execute(query).commit()
    query = "EXECUTE contabyx.contabyx.delete_null_from_transfers"
    cursor.execute(query).commit()

if __name__ == '__main__':
    main()