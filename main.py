from flask import Flask, render_template, request, redirect, url_for
import requests
import openai
import os
from dotenv import load_dotenv
import dotenv
app = Flask(__name__)

load_dotenv(override=True)
api_key = dotenv.get_key(".env", "OPENAI_API_KEY")
print(api_key)

@app.route('/campaign', methods=['GET', 'POST'])
def campaign():
    if request.method == 'POST':
        campaign_name = request.form['campaign_name']
        num_players = request.form['num_players']
        format = request.form['format']
        length = request.form['length']
        campaign_type = request.form['type']
        return redirect(url_for('confirm', campaign_name=campaign_name, num_players=num_players, format=format, length=length))
    return render_template('campaign.html')

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        campaign_name = request.form['campaign_name']
        num_players = request.form['num_players']
        length = request.form['length']
        campaign_type = request.form['type']
        format = request.form['format']
        prompt = generate_prompt(campaign_name, num_players, format, length, campaign_type)
        campaign = generate_campaign(prompt)
        return render_template('confirm.html', prompt=prompt, campaign=campaign)
    else:
        return redirect(url_for('campaign'))

@app.route('/charactersheet', methods=['GET', 'POST'])
def charactersheet():
    if request.method == 'POST':
        # Process the form data and generate prompts to ChatGPT
        name = request.form['name']
        race = request.form['race']
        class_ = request.form['class']
        alignment = request.form['alignment']
        stats = {}
        stats['str'] = int(request.form['str'])
        stats['dex'] = int(request.form['dex'])
        stats['con'] = int(request.form['con'])
        stats['int'] = int(request.form['int'])
        stats['wis'] = int(request.form['wis'])
        stats['cha'] = int(request.form['cha'])
        starting_spells = request.form['starting-spells']
        # Generate prompts using the form data
        prompt = generate_prompt(name, race, class_, alignment, stats, starting_spells)
        completion = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completion.choices[0].text.strip()
        # Render the response as HTML
        return render_template('charactersheet_response.html', response=response)
    else:
        # Render the character sheet HTML form
        return render_template('charactersheet.html')



def generate_campaign(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3900,
        n=1,
        stop=None,
        temperature=1,
    )

    campaign = response.choices[0].text.strip()
    return campaign




@app.route('/')
def index():
    return render_template('index.html')


def generate_prompt(campaign_name, num_players, format, length, campaign_type):
    prompt = f"Create a {format} DND/Pathfinder-like campaign called '{campaign_name}' for {num_players} players in which each session(s) lasts {length} hours. The campaign should include a variety of encounters and NPCs for the players to interact with and follow the theme given. This is the description given by the DM:'{campaign_type}."
    return prompt


if __name__ == '__main__':
    app.run(debug=True)
