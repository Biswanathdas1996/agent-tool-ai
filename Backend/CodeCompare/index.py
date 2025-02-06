# import requests
# from flask import request, jsonify, send_file
# from Gemini.gemini import call_gemini

# def get_pr_code_changes(owner, repo, pr_number):
    
#     url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch PR data: {response.status_code}, {response.text}")
    
#     files = response.json()
#     code_changes = ""
    
#     for file in files:
#         filename = file["filename"]
#         patch = file.get("patch", "No patch available")
        
#         code_changes += f"\nFile: {filename}\n{patch}\n"
    
#     return code_changes


# def submit_to_compare_code():
#     try:
#         data = request.get_json()

#         owner = data.get('owner')
#         repo = data.get('repo')
#         pr_number = data.get('pr_number')
#         user_story = data.get('user_story')
        
        

#         if not owner:
#             return jsonify({'error': 'owner is required'}), 400
#         if not repo:
#             return jsonify({'error': 'repo is required'}), 400
#         if not pr_number:
#             return jsonify({'error': 'pr_number is required'}), 400
        
#         # # Example usage:
#         # owner = "Biswanathdas1996"
#         # repo = "agent-tool"
#         # pr_number = 1

#         changes = get_pr_code_changes(owner, repo, pr_number)
#         print(changes)

#         prompt = f"""
#         Compare the code changes in the PR with the user story below and provide feedback in a html format on the code changes.

#         give missing points in the code changes
#         suggest improvements in the code changes
#         give feedback on the code changes

#         give a revised code conceding the missing points
#         add the code inside the <code> or <pre> tag
#         user story: {user_story}

#         code changes:{changes}

#         """
#         llm_result = call_gemini(prompt)

#         return jsonify({'result': llm_result}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# def render_code_compare_pack(app):
#     app.add_url_rule('/compare-user-story-code', 'submit_to_compare_code_api', submit_to_compare_code, methods=['POST'])
#     return app


import requests
from flask import request, jsonify, send_file
from Gemini.gemini import call_gemini

def get_pr_code_changes(owner, repo, pr_number):
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR data: {response.status_code}, {response.text}")
    
    files = response.json()
    code_changes = ""
    
    for file in files:
        filename = file["filename"]
        patch = file.get("patch", "No patch available")
        
        code_changes += f"\nFile: {filename}\n{patch}\n"
    print ("----------------------------",code_changes)
    return code_changes


def submit_to_compare_code():
    try:
        data = request.get_json()

        owner = data.get('owner')
        repo = data.get('repo')
        pr_number = data.get('pr_number')
        user_story = data.get('user_story')
        
        

        if not owner:
            return jsonify({'error': 'owner is required'}), 400
        if not repo:
            return jsonify({'error': 'repo is required'}), 400
        if not pr_number:
            return jsonify({'error': 'pr_number is required'}), 400


        changes = get_pr_code_changes(owner, repo, pr_number)
        print("---------------", changes)
        
        prompt = f"""
        Compare the code changes in the PR with the user story below and provide structured feedback in the following HTML format:

        <article>
            <header>
                <h1>Code Review Feedback</h1>
                <p><strong>File:</strong> [Mention filename from PR in which review is being done.]</p>
            </header>
            <section>
                <h2>Missing Points</h2>
                <ul>
                    <li>List down the point specifically , that is missing on the code but present in the user story</li>
                </ul>
            </section>
            <section>
                <h2>Missing Functionalities</h2>
                <ul>
                    <li>List down the Functionalities , that is missing on the code but mentioned in the user story, for example any input field / and ui elements</li>
                </ul>
            </section>
            <section>
                <h2>Suggested Improvements</h2>
                <ul>
                    <li>[Provide improvement suggestions]</li>
                </ul>
            </section>
            <section>
                <h2>Code Alignment with User Story</h2>
                <p>[Explain how well the code aligns with the user story, mentioning any deviations]</p>
            </section>
            <section>
                <h2>Code Comparison</h2>
                <div style="display: flex; gap: 10px;">
                    <div style="width: 100%;">
                        <h3>Modified Code</h3>
                        <textarea style="width: 100%; height: 400px;" readonly>[Complete revised code that fully adheres to the user story, incorporating all missing elements.]</textarea>
                    </div>
                </div>
            </section>
            <section>
                <h2>Points Added in Revised Code</h2>
                <ul>
                    <li>[Provide the exact lines of code added in the revised version]</li>
                </ul>
            </section>
            <section>
                <h2>Overall Code Quality Assessment</h2>
                <p>[Provide insights on maintainability, readability, performance, and adherence to best practices]</p>
            </section>
        </article>

        User Story:
        {user_story}

        Code Changes:
        {changes}
        
        instructions to be followed:
        - Structure strictly in above mentioned format.
        - Ensure to provide revised code that adheres completely with user story with implementing all missing fields and elements.
        - Ensure that the revised code is complete, correct, and structured according to best practices.
        
        
        """


        
        



        llm_result = call_gemini(prompt)
        print("=====================",llm_result)
        return jsonify({'result': llm_result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def render_code_compare_pack(app):
    app.add_url_rule('/compare-user-story-code', 'submit_to_compare_code_api', submit_to_compare_code, methods=['POST'])
    return app



