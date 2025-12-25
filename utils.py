def find_relevant_schemes(user_query, schemes):
    matches = []
    query = user_query.lower()

    for scheme in schemes:
        if scheme["name"].lower() in query:
            matches.append(scheme)
        else:
            for kw in scheme.get("keywords", []):
                if kw in query:
                    matches.append(scheme)
                    break

    return matches
