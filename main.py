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
