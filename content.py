# Authored content for the new site: pupil needs, Individual Development pages, evidence ratings.

NEEDS = [
 ("forgetting", "Pupils forget what they have been taught",
  "Pupils can answer soon after teaching but struggle weeks later, or start new topics without the knowledge they need.",
  "Forgetting is normal. Retrieval and spacing make knowledge more durable and show you what needs revisiting. Start by making the Do Now genuine retrieval from memory, then plan when key knowledge comes back.",
  ["DN01","DN02","DN03","DN04","FI08","DN07"]),
 ("participation", "Only a few pupils answer questions",
  "The same hands go up, quieter pupils rarely contribute, and you are not sure the rest of the class is thinking.",
  "Make thinking everyone's job. Give time to think, then use a routine that expects every pupil to be ready to answer. Make it safe to be wrong.",
  ["DT01","DT02","DT08","CA01","DT11","CC11","DT09"]),
 ("checking", "I can't tell who has understood",
  "Answers from a few pupils leave you unsure whether the class is ready to move on, and errors surface later in independent work.",
  "Collect evidence from every pupil at the points where it would change your next decision, then act on what you see.",
  ["CA01","CA02","CA03","LP04","CA05","CA06"]),
 ("independence", "Pupils struggle when working independently",
  "Pupils seem to follow the model but make many errors, stall or ask for help as soon as they work alone.",
  "Independence is built in stages. Show a complete model, practise together, check readiness, then remove support deliberately.",
  ["EX08","EX07","PR01","PR02","PR03","CA09","PR07"]),
 ("explanations", "Pupils don't follow my explanations",
  "Explanations feel clear to you, but pupils lose the thread, cannot repeat the key idea or need it explained again.",
  "Reduce what pupils have to hold in mind at once. Break content into small steps, make expert thinking visible and remove anything that competes for attention.",
  ["EX01","EX09","EX03","EX02","EX10","EX05","EX04"]),
 ("misconceptions", "Pupils keep making the same mistakes",
  "The same errors recur across lessons and assessments, even after you have corrected them.",
  "Plan for the misconception before the lesson, expose it deliberately and check the fix on a fresh question. Feedback only helps when pupils act on it.",
  ["LP03","LP04","CA06","CA11","FI01","FI05","FI06"]),
 ("routines", "Learning time is lost at the start, transitions or end",
  "Lessons start slowly, attention drifts during instructions and transitions take longer than they should.",
  "Consistent, rehearsed routines protect attention and learning time. Use the agreed BSCS routines first, then teach and rehearse any that are unreliable.",
  ["CC01","CC03","CC07","CC09","CC02","CC10","CC06"]),
 ("precision", "Pupils' answers are short or imprecise",
  "Answers are one word, vague or partly correct, and pupils rarely use subject vocabulary accurately.",
  "Raise the expectation of what a complete answer sounds like, give pupils the words to say it, and ask them to improve their own answer.",
  ["DT06","DT12","EX06","DT10","DT07","CC04"]),
 ("access", "Some pupils can't access the task, or need more challenge",
  "The same task leaves some pupils stuck and others finished early, and adaptations risk lowering the goal.",
  "Keep the goal ambitious for everyone. Check prerequisites, scaffold the specific barrier and plan how support will be removed or challenge increased.",
  ["LP02","LP05","CA07","PR03","PR08","PR11"]),
 ("feedback", "Feedback isn't improving pupils' work",
  "You spend time giving feedback, but the same issues reappear and pupils don't use the comments.",
  "Feedback works when pupils act on it. Focus on the most important next step, plan time for pupils to improve, and check the improvement on a new task.",
  ["FI02","FI01","FI05","FI06","FI03","FI07"]),
]

TIERS = {
 "S": ("Strong evidence base", "tier-s",
       "This strategy applies an approach with a strong, consistent research base, such as high-security EEF evidence or well-replicated findings from cognitive science. Research on this exact routine may be more limited, so check how your pupils respond."),
 "R": ("Research-informed", "tier-r",
       "This strategy is consistent with research principles, but the evidence for this kind of practice is less direct, more mixed or more dependent on context."),
 "P": ("Established practice", "tier-p",
       "This strategy is mainly based on expert practitioner experience and agreed BSCS routines. Research supports the underlying principles indirectly."),
}

CORE_TEXT = ("Core strategies combine the strongest evidence with the BSCS teaching model's priorities. "
             "They are a good place to start, but your choice should still come from what your pupils need.")

# Develop pages: (slug, title, lede, html body)
DEVELOP_INTRO = """
<p>Individual Development CPD gives you protected time to improve one specific aspect of your classroom practice. You choose a focus from your PGD, try a small change, use peer observation to see what happens and refine your approach across the year.</p>
<p>This site is designed to help at every stage. Each strategy page includes an example goal, what a peer observer could look for and a quick way to check whether the change is helping pupils.</p>
<h2 id="the-cycle">The improvement cycle</h2>
<ol class="cycle">
<li><strong>Identify.</strong> Name a pupil learning problem you can see in your classroom, and what pupils should do differently.</li>
<li><strong>Explore.</strong> Use the <a href="{p}needs/">pupil needs</a> pages or the <a href="{p}strategies/">strategy library</a> to find evidence-informed options.</li>
<li><strong>Plan.</strong> Choose one small, precise change. Write it as <em>I will … so that students …</em></li>
<li><strong>Implement.</strong> Practise the change in normal lessons until it feels routine.</li>
<li><strong>Observe.</strong> A colleague gathers focused evidence on your change and how pupils respond.</li>
<li><strong>Reflect.</strong> Look at what pupils did differently. Separate how well you implemented the change from its effect on pupils.</li>
<li><strong>Adapt.</strong> Refine the change, embed it, or try something different in the next cycle.</li>
</ol>
<h2 id="keep-it-manageable">Keep it manageable</h2>
<ul>
<li>One change at a time. A precise, small change you practise often beats several new ideas at once.</li>
<li>Use the look-fors on each strategy page instead of writing your own observation form.</li>
<li>Pupil work, mini-whiteboard responses and short checks are enough evidence. You do not need a formal research project.</li>
</ul>
<div class="card-row">
<a class="link-card" href="{p}develop/writing-your-goal/"><span class="eyebrow">Step 1–3</span><strong>Write a precise goal</strong><span>From a broad aim to one observable change.</span></a>
<a class="link-card" href="{p}develop/peer-observation/"><span class="eyebrow">Step 5</span><strong>Peer observation</strong><span>A developmental, focused protocol.</span></a>
<a class="link-card" href="{p}develop/evaluating-impact/"><span class="eyebrow">Steps 6–7</span><strong>Evaluate and adapt</strong><span>Is the change helping pupils?</span></a>
</div>
"""

DEVELOP_GOAL = """
<p>Your classroom-based Professional Growth focus should connect what you will do with what will be different for pupils. Use this structure:</p>
<p class="formula">I will <strong>[specific change in my practice]</strong> so that students <strong>[observable response or outcome]</strong>.</p>
<h2 id="four-steps">Four steps to a precise goal</h2>
<table>
<tr><th scope="col">Step</th><th scope="col">Ask yourself</th><th scope="col">Example</th></tr>
<tr><td>1. Pupil problem</td><td>What are pupils doing that limits learning, or not yet doing that would improve it?</td><td>Pupils in my lower-attaining classes are not engaging in Turn and Talk.</td></tr>
<tr><td>2. Possible cause</td><td>Why might this be happening? Consider knowledge, confidence, routines, modelling, scaffolding, practice or feedback. You do not need to be right yet.</td><td>They may lack confidence, a clear routine or the knowledge to discuss.</td></tr>
<tr><td>3. Practice change</td><td>What one change could you make? Browse the <a href="{p}needs/">pupil needs</a> pages for options.</td><td>Model a strong response, give a sentence stem and cold call pairs afterwards.</td></tr>
<tr><td>4. Write the goal</td><td>Does it link a teacher action to a pupil outcome?</td><td>I will structure Turn and Talk with a modelled response and a sentence stem so that students give more developed answers.</td></tr>
</table>
<h2 id="broad-to-precise">From broad to precise</h2>
<table>
<tr><th scope="col">Too broad</th><th scope="col">Precise and observable</th></tr>
<tr><td>Improve my questioning.</td><td>I will use question–pause–name cold calling with five seconds of thinking time so that more students prepare an answer and give fuller responses.</td></tr>
<tr><td>Use more checking for understanding.</td><td>I will use a mini-whiteboard check after each explanation chunk so that I can see every student's answer and fix errors before independent practice.</td></tr>
<tr><td>Improve independent practice.</td><td>I will protect at least 15 minutes for independent practice so that students complete enough practice and I can see what they can do without support.</td></tr>
<tr><td>Better scaffolding.</td><td>I will fade prompts across worked examples so that students can reproduce the process independently and explain each step.</td></tr>
</table>
<h2 id="avoid">Avoid</h2>
<ul>
<li><strong>Strategy-only goals</strong> such as "improve behaviour management", which say nothing about pupils.</li>
<li><strong>Lists of several vague aims.</strong> Choose one focus you can observe.</li>
<li><strong>Goals that cannot be seen in a lesson.</strong> A peer should be able to observe your change and pupils' responses.</li>
</ul>
<p>Every <a href="{p}strategies/">strategy page</a> includes an example goal in this format. Use it as a starting point and adapt it to your class.</p>
"""

DEVELOP_OBS = """
<p>Peer observation in Individual Development is developmental, not judgemental. The observer gathers focused evidence on one change and how pupils respond. There are no grades and no whole-lesson judgements.</p>
<h2 id="before">Before the observation (5 minutes)</h2>
<ul>
<li>Share your goal: <em>I will … so that students …</em></li>
<li>Agree when in the lesson the strategy will be used.</li>
<li>Agree two or three look-fors. Each strategy page suggests some, covering what you will do and how pupils should respond.</li>
</ul>
<h2 id="during">During the observation</h2>
<ul>
<li>Focus only on the agreed part of the lesson and the agreed look-fors.</li>
<li>Record what you see and hear, not opinions: what the teacher said or did, and what pupils did in response.</li>
<li>Note examples of pupil responses: answers on boards, quality of talk, errors, how many pupils were involved.</li>
</ul>
<h2 id="after">After the observation (10 minutes)</h2>
<ol>
<li><strong>What did you notice?</strong> The observer shares evidence against each look-for.</li>
<li><strong>How did pupils respond?</strong> Discuss what the evidence suggests about pupils' learning.</li>
<li><strong>What next?</strong> Agree one precise refinement to try before the next observation.</li>
</ol>
<h2 id="prompts">Useful dialogue prompts</h2>
<ul>
<li>"When you did …, I saw pupils …"</li>
<li>"How many pupils were able to …?"</li>
<li>"What would you change about the timing or wording?"</li>
<li>"What will you look for in pupils' work this week?"</li>
</ul>
<p class="note">Keep observation notes developmental and between colleagues. Do not record identifiable pupil information beyond what is needed for professional discussion.</p>
"""

DEVELOP_EVAL = """
<p>The aim is not to prove that a strategy works, but to find out whether it is helping <em>your</em> pupils and what to do next. Keep two questions separate.</p>
<div class="two-col">
<div class="panel"><h3>1. Am I doing it as intended?</h3><p>This is <strong>implementation</strong> evidence: how consistently and precisely you are using the strategy. Peer observation and self-review help here.</p></div>
<div class="panel"><h3>2. Is it helping pupils?</h3><p>This is <strong>impact</strong> evidence: what pupils now do, know or produce differently. Look at pupil responses and work.</p></div>
</div>
<h2 id="simple-evidence">Simple sources of evidence</h2>
<ul>
<li>Mini-whiteboard or hinge question responses on first attempt and re-check.</li>
<li>Do Now or quiz scores on revisited items over several weeks.</li>
<li>Samples of pupil work before and after the change.</li>
<li>Who contributes, and how fully, over several lessons.</li>
<li>Time taken for routines or for all pupils to start work.</li>
</ul>
<p>Each strategy page suggests a quick check of impact. Choose one and use it consistently.</p>
<h2 id="interpret-carefully">Interpret carefully</h2>
<ul>
<li>Busy, compliant pupils or completed tasks are not the same as secure learning.</li>
<li>Early changes may be small. Look for direction of travel across several lessons.</li>
<li>Other factors affect pupil outcomes. Avoid claiming a single change caused improvement in attainment.</li>
</ul>
<h2 id="decide">Decide what next</h2>
<table>
<tr><th scope="col">If…</th><th scope="col">Then…</th></tr>
<tr><td>The strategy is used well and pupils are responding</td><td><strong>Embed</strong> it, then extend it to another class or a related step.</td></tr>
<tr><td>The strategy is used inconsistently</td><td><strong>Refine</strong> the implementation. Practise the specific step, script it or use a prompt.</td></tr>
<tr><td>It is used well but pupils are not responding</td><td><strong>Rethink.</strong> Revisit the cause of the problem and choose a different strategy.</td></tr>
</table>
"""
