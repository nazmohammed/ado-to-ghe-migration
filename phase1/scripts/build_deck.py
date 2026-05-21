"""Generate Phase 1 ADO -> GHE migration PowerPoint deck."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Brand palette - Saudi Ministry of Justice
MOJ_GREEN  = RGBColor(0x38, 0x79, 0x6B)  # primary brand green
MOJ_DARK   = RGBColor(0x1F, 0x4D, 0x42)  # darker for headers/footers
MOJ_LIGHT  = RGBColor(0x7F, 0xB5, 0xA6)  # lighter accent
NAVY    = MOJ_DARK
TEAL    = MOJ_GREEN
AMBER   = RGBColor(0xD4, 0xA8, 0x4B)     # warm gold accent (complements green)
RED     = RGBColor(0xB0, 0x3A, 0x2E)
GREEN   = RGBColor(0x2E, 0x86, 0x4B)
LGREY   = RGBColor(0xF2, 0xF4, 0xF7)
MGREY   = RGBColor(0xCB, 0xD2, 0xD9)
DGREY   = RGBColor(0x4A, 0x55, 0x68)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BLACK   = RGBColor(0x10, 0x18, 0x28)
LOGO_PATH = r"C:\Users\nazmohammed\.copilot\session-state\f7603c23-d320-431c-874f-087287e33674\files\moj-logo.png"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

BLANK = prs.slide_layouts[6]


# ---------- helpers ----------
def add_rect(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.5)
    shp.shadow.inherit = False
    return shp


def add_text(slide, x, y, w, h, text, size=14, bold=False, color=BLACK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(text, str):
        lines = [text]
    else:
        lines = text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return tb


def slide_header(slide, title, subtitle=None):
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.9), NAVY)
    # Logo in header (top-left)
    try:
        slide.shapes.add_picture(LOGO_PATH, Inches(0.15), Inches(0.1),
                                 height=Inches(0.7))
    except Exception:
        pass
    add_text(slide, Inches(2.3), Inches(0.12), Inches(10.7), Inches(0.5),
             title, size=24, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        add_text(slide, Inches(2.3), Inches(0.55), Inches(10.7), Inches(0.3),
                 subtitle, size=12, color=MGREY, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(slide, 0, Inches(0.9), SLIDE_W, Inches(0.05), TEAL)


def slide_footer(slide, num, total, deck="Saudi MoJ  |  ADO -> GHE  |  Phase 1 Plan"):
    add_text(slide, Inches(0.3), Inches(7.15), Inches(8), Inches(0.3),
             deck, size=9, color=DGREY)
    add_text(slide, Inches(12.0), Inches(7.15), Inches(1.2), Inches(0.3),
             f"{num} / {total}", size=9, color=DGREY, align=PP_ALIGN.RIGHT)


def add_table(slide, x, y, w, h, data, header=True, col_widths=None,
              font_size=11, header_fill=NAVY, header_color=WHITE,
              zebra=True, zebra_fill=LGREY):
    rows = len(data)
    cols = len(data[0])
    tbl_shape = slide.shapes.add_table(rows, cols, x, y, w, h)
    tbl = tbl_shape.table
    if col_widths:
        total = sum(col_widths)
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = int(w * cw / total)
    for r_i, row in enumerate(data):
        for c_i, val in enumerate(row):
            cell = tbl.cell(r_i, c_i)
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            if header and r_i == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill
                fcolor = header_color
                fbold = True
            else:
                if zebra and r_i % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = zebra_fill
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = WHITE
                fcolor = BLACK
                fbold = False
            tf = cell.text_frame
            tf.word_wrap = True
            tf.text = str(val)
            for para in tf.paragraphs:
                para.alignment = PP_ALIGN.LEFT
                for run in para.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(font_size)
                    run.font.bold = fbold
                    run.font.color.rgb = fcolor
    return tbl


slides_total = 18
slide_num = 0

SPEAKER_NOTES = {
    1: "Welcome and framing. Today we are walking through the detailed Phase 1 plan to migrate 100 Azure DevOps repositories to GitHub Enterprise, keeping Boards and release pipelines in Azure DevOps. Key message: this is the lowest-risk path. We move code only, and we preserve the existing release investment.",
    2: "Frame what is in and out. In scope: 100 repos with full history, PRs, commits, LFS; MoJ Entra SSO + SCIM; rulesets replacing ADO branch policies; ADO Pipelines re-pointed at GitHub source; Azure Boards GitHub App for AB#123 linking. Deferred to Phase 2: anything that touches CI/CD or work-item migration. Headline numbers: 10 weeks, 8 people, 5.3 peak FTE, 150 person-days.",
    3: "The architecture is deliberately hybrid. GitHub Enterprise (EMU) becomes the source of truth for code. Azure DevOps keeps work items, boards, pipelines, releases, service connections, artifacts, and wikis. MoJ Entra ID authenticates both ends. The Azure Boards GitHub App is the wire between the two systems and is what makes the hybrid feel seamless to developers.",
    4: "The integration is what removes the main objection to splitting code from work items. Developers type AB#123 in a commit, branch, or PR. The Boards App sees it, and both sides show the link. On PR merge, the linked work item auto-transitions state. We verify all five capabilities listed during the pilot wave before scaling.",
    5: "Walk through each pre-requisite category. Highlight commercial (EMU contract must be signed before Week 1), identity (book MoJ Entra admin now), source-side (PCA on all ADO orgs), target-side (orgs pre-created, ruleset JSON approved), tooling (gh-gei + gh-ado2gh installed), network (proxy whitelist), governance (sponsor + steering), and pipelines (Azure Pipelines GitHub App approval). If any of these slips, the program slips 1:1.",
    6: "Walk through the Gantt. Five stages over 10 weeks. M2 is the critical gate -- identity foundation -- because everything downstream depends on EMU + SAML + SCIM being live. Waves 1-4 overlap in weeks 7-9, with a hard cap of two waves in flight at any time to protect hypercare capacity.",
    7: "Eight people, 5.3 peak FTE. Note the gap between 217 capacity person-days and 150 effort person-days -- that's normal slack for change-heavy work. Tech Lead and the two Platform Engineers are the largest contributors. The IAM Engineer is the smallest contributor by p-days but the highest-risk single point of failure -- their availability in weeks 3-4 is non-negotiable. Roles outside the 8 (sponsor, ADO admins, repo owners) are on-demand consultees, not delivery headcount.",
    8: "Heatmap shows when each role is hot. IAM peaks in Stage 1. Platform Eng pair peak in Stages 2 and 3. DevEx peaks in Stages 2 and 3 (pipeline re-pointing). Change Manager peaks at Stage 0 (comms plan + templates) and then settles to normal. Bottom strip: book a backup IAM resource for weeks 3-4.",
    9: "Workstream breakdown. PMO and Repo Migration are the two largest cost centres at 25 p-days each. Pipeline re-pointing is 20 p-days and is the line item most likely to slip if the Classic-pipeline ratio is high. Comms and Training (15 p-days) is consistently underestimated in this kind of program -- be ruthless about not cutting it.",
    10: "L1 milestones. Five gates, each with explicit exit criteria. The critical path runs through M2 (identity foundation). If M2 slips, everything slips. The mitigation -- book MoJ IAM resource at kickoff -- is on the next slide as Decision D8.",
    11: "L2 breakdown for Stages 0 and 1. Stage 0 is parallel discovery streams (repos, pipelines, policies, identity). Stage 1 is identity foundation and migration factory build. The end-to-end factory smoke test against a throwaway repo is the gate that authorises the pilot.",
    12: "L2 for the pilot wave. 17 activities. Two-thirds of the value of the pilot is in step 13 (smoke tests + sign-off by repo owners) and step 14 (3 days of hypercare). Do not skip them. The pilot retrospective at step 16 feeds runsheet updates that all four production waves consume.",
    13: "L2 for production waves. Per-wave template is ~11 p-days, repeated four times. Two waves overlap in flight. Total Stage 3 effort is ~44 p-days in a 3-week calendar window. The strict 'no new wave during another wave's D-0 to D+3' rule is what stops hypercare from collapsing.",
    14: "Illustrative L3 cut for Stage 0 -- 19 tasks. The full L3 is ~80 tasks across all five stages. Each task has owner, effort, and predecessor. The CSV export of the full L3 is available alongside this deck for import into project tooling.",
    15: "Top 10 risks. R1 (IAM availability) and R2 (Classic pipelines) are the schedule risks. R5 (LFS / oversize repos) is the data-integrity risk -- audit early. R8 (concurrent waves overloading hypercare) is the operational risk that the wave cadence rule mitigates. R10 (pipeline secrets) is the silent risk -- builds will look fine until they try to deploy.",
    16: "Ten decisions for steering to close in week 1. D2 (GHAS in or out) drives security baseline. D3 (disable Issues) prevents work-item drift. D4 (mannequin policy) sets expectations for ex-staff. D7 (concurrent waves cap) protects hypercare. D8 (backup IAM) is the single most important risk mitigation.",
    17: "Phase 2 is intentionally out of scope. CI/CD migration to GitHub Actions, runners on VMSS, OIDC to Azure, and Azure Pipelines decommission. Indicative 12-16 weeks and 200-250 p-days. The detailed Phase 2 estimate must be produced at M5 close, not now -- we won't know actual pipeline counts and complexity until we have walked through them in Phase 1.",
    18: "Seven next steps to authorise Week 1. The two that have lead time are step 3 (EMU procurement) and step 5 (booking MoJ Entra admin). Both must start now, before steering signs off scope, or they will become the schedule bottleneck.",
}



# ---------- 1. Title ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, MOJ_DARK)
# Decorative bands
add_rect(s, 0, Inches(3.0), SLIDE_W, Inches(0.06), MOJ_GREEN)
add_rect(s, 0, Inches(4.5), SLIDE_W, Inches(0.06), AMBER)
# Logo top-left, larger on title
try:
    s.shapes.add_picture(LOGO_PATH, Inches(0.5), Inches(0.4), height=Inches(1.3))
except Exception:
    pass
add_text(s, Inches(0.6), Inches(1.95), Inches(12), Inches(1.0),
         "Azure DevOps -> GitHub Enterprise", size=40, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(2.7), Inches(12), Inches(0.7),
         "Phase 1 Migration Plan & Effort Estimation", size=26, color=MGREY)
add_text(s, Inches(0.6), Inches(3.55), Inches(12), Inches(0.5),
         "100 Repositories  |  Repos + PRs + Commits  |  MoJ Entra ID",
         size=18, color=AMBER, bold=True)
add_text(s, Inches(0.6), Inches(4.9), Inches(12), Inches(0.5),
         "Boards & Release Pipelines remain in Azure DevOps", size=16, color=WHITE)
add_text(s, Inches(0.6), Inches(5.4), Inches(12), Inches(0.5),
         "Azure Boards GitHub App wires the two ends together", size=16, color=WHITE)
add_text(s, Inches(0.6), Inches(6.5), Inches(12), Inches(0.35),
         "Saudi Arabia Ministry of Justice  |  Platform Engineering", size=12, bold=True, color=AMBER)
add_text(s, Inches(0.6), Inches(6.85), Inches(12), Inches(0.35),
         "Version 1.0", size=10, color=MGREY)


# ---------- 2. Executive Summary ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Executive Summary", "What we are doing, and what we are deliberately not doing in Phase 1")

# Left card - In scope
add_rect(s, Inches(0.4), Inches(1.2), Inches(6.2), Inches(2.7), LGREY)
add_rect(s, Inches(0.4), Inches(1.2), Inches(6.2), Inches(0.45), GREEN)
add_text(s, Inches(0.55), Inches(1.25), Inches(6), Inches(0.4),
         "IN SCOPE - PHASE 1", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(1.75), Inches(6), Inches(2.1),
         ["- 100 ADO repositories migrated to GHE (EMU)",
          "- Full commit history, all branches, all tags",
          "- Open + closed Pull Requests with comments",
          "- LFS objects and attachments",
          "- MoJ Entra ID SSO + SCIM provisioning",
          "- Branch protection re-implemented as GHE rulesets",
          "- Azure Pipelines re-pointed to GitHub source",
          "- Azure Boards GitHub App for AB#123 linking"],
         size=12, color=BLACK)

# Right card - Out of scope (Phase 2)
add_rect(s, Inches(6.8), Inches(1.2), Inches(6.2), Inches(2.7), LGREY)
add_rect(s, Inches(6.8), Inches(1.2), Inches(6.2), Inches(0.45), AMBER)
add_text(s, Inches(6.95), Inches(1.25), Inches(6), Inches(0.4),
         "DEFERRED TO PHASE 2", size=13, bold=True, color=BLACK, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(6.95), Inches(1.75), Inches(6), Inches(2.1),
         ["- Migrate CI / Build pipelines to GitHub Actions",
          "- Migrate Release pipelines to Actions Environments",
          "- Self-hosted runners (Azure VMSS) at scale",
          "- OIDC federation to Azure subscriptions",
          "- Decommission Azure Pipelines & Releases",
          "- Migrate work items / Boards (only if requested)",
          "- Org consolidation (95 ADO -> N GHE orgs)"],
         size=12, color=BLACK)

# Bottom KPI strip
y0 = Inches(4.2)
kpis = [
    ("10", "weeks duration"),
    ("8", "team members"),
    ("~5.3", "peak FTE"),
    ("150", "person-days effort"),
    ("4 + Pilot", "migration waves"),
    ("5", "L1 milestones"),
]
gap = Inches(0.1)
card_w = (SLIDE_W - Inches(0.8) - gap * (len(kpis) - 1)) / len(kpis)
for i, (val, label) in enumerate(kpis):
    x = Inches(0.4) + i * (card_w + gap)
    add_rect(s, x, y0, card_w, Inches(1.2), NAVY)
    add_text(s, x, y0 + Inches(0.1), card_w, Inches(0.55),
             val, size=28, bold=True, color=AMBER,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x, y0 + Inches(0.7), card_w, Inches(0.5),
             label, size=11, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_rect(s, Inches(0.4), Inches(5.6), Inches(12.5), Inches(1.4), LGREY)
add_text(s, Inches(0.55), Inches(5.65), Inches(12.3), Inches(0.35),
         "STRATEGIC POSITION", size=11, bold=True, color=TEAL)
add_text(s, Inches(0.55), Inches(5.95), Inches(12.3), Inches(1.0),
         ["Phase 1 is the lowest-risk path to land 100 repos behind MoJ SSO while preserving the existing CD investment.",
          "ADO Pipelines & Releases continue unchanged; only the source repository is re-pointed to GitHub.",
          "Azure Boards stays as the work-management system of record; AB#123 references keep traceability intact."],
         size=12, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 3. Phase 1 Architecture ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Target Architecture - Phase 1", "Hybrid model: code in GitHub, work items + releases in Azure")

# MoJ Entra at top
add_rect(s, Inches(4.5), Inches(1.3), Inches(4.3), Inches(0.7), TEAL)
add_text(s, Inches(4.5), Inches(1.3), Inches(4.3), Inches(0.7),
         "MoJ Microsoft Entra ID", size=14, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Left - GitHub Enterprise
add_rect(s, Inches(0.5), Inches(2.4), Inches(5.8), Inches(3.6), LGREY)
add_rect(s, Inches(0.5), Inches(2.4), Inches(5.8), Inches(0.5), NAVY)
add_text(s, Inches(0.5), Inches(2.4), Inches(5.8), Inches(0.5),
         "GitHub Enterprise (EMU)", size=13, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.7), Inches(3.0), Inches(5.5), Inches(3.0),
         ["- 100 repositories (1:1 with ADO orgs)",
          "- Commits, branches, tags, history",
          "- Pull Requests + comments",
          "- LFS + attachments",
          "- Rulesets (replicating ADO branch policies)",
          "- CODEOWNERS",
          "- Optional: GitHub Advanced Security"],
         size=12, color=BLACK)

# Right - Azure DevOps
add_rect(s, Inches(7.0), Inches(2.4), Inches(5.8), Inches(3.6), LGREY)
add_rect(s, Inches(7.0), Inches(2.4), Inches(5.8), Inches(0.5), RGBColor(0x00, 0x78, 0xD4))
add_text(s, Inches(7.0), Inches(2.4), Inches(5.8), Inches(0.5),
         "Azure DevOps", size=13, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(7.2), Inches(3.0), Inches(5.5), Inches(3.0),
         ["- Work Items + Boards (unchanged)",
          "- Build pipelines (source -> GitHub)",
          "- Release pipelines (unchanged)",
          "- Service connections to Azure (unchanged)",
          "- Artifacts feeds (unchanged)",
          "- Wikis (unchanged for now)"],
         size=12, color=BLACK)

# Bridge text
add_rect(s, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.7), AMBER)
add_text(s, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.7),
         "Azure Boards GitHub App -- AB#123 references link commits / PRs / branches both ways and auto-transition work item state on PR merge",
         size=12, bold=True, color=BLACK,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

slide_footer(s, slide_num, slides_total)


# ---------- 4. Boards Integration ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Azure Boards <-> GitHub Linking",
             "How AB#123 references keep work items in ADO and code in GitHub stitched together")

# Flow
flow_y = Inches(1.5)
boxes = [
    ("Developer commits / opens PR\nin GitHub", LGREY, BLACK),
    ("Mentions AB#123 in commit msg,\nPR title, or branch name", LGREY, BLACK),
    ("Azure Boards GitHub App\ndetects reference", TEAL, WHITE),
    ("ADO work item links to the\nGitHub PR / commit / branch", LGREY, BLACK),
    ("On PR merge, ADO work item\nauto-transitions state", GREEN, WHITE),
]
gap = Inches(0.15)
bw = (SLIDE_W - Inches(0.8) - gap * (len(boxes) - 1)) / len(boxes)
for i, (txt, fill, color) in enumerate(boxes):
    x = Inches(0.4) + i * (bw + gap)
    add_rect(s, x, flow_y, bw, Inches(1.8), fill)
    add_text(s, x, flow_y, bw, Inches(1.8),
             txt, size=11, bold=True, color=color,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(boxes) - 1:
        arr_x = x + bw + Inches(0.005)
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                 arr_x, flow_y + Inches(0.85),
                                 gap - Inches(0.01), Inches(0.2))
        arr.fill.solid()
        arr.fill.fore_color.rgb = NAVY
        arr.line.fill.background()

# Capability table
add_text(s, Inches(0.4), Inches(3.8), Inches(12.5), Inches(0.4),
         "Capabilities provided by the integration", size=14, bold=True, color=NAVY)
cap_data = [
    ["Capability", "Works?", "Notes"],
    ["Link GitHub PR <-> ADO work item", "Yes", "Two-way visibility on both platforms"],
    ["Link GitHub commit <-> ADO work item", "Yes", "Reference in commit message"],
    ["Link GitHub branch <-> ADO work item", "Yes", "Reference in branch name"],
    ["Auto-state-transition on PR merge", "Yes", "Configurable via ADO process template"],
    ["Multiple ADO projects -> one GHE org", "Yes", "Multi-project mapping supported"],
    ["Multiple GHE orgs -> one ADO org", "Yes", "Install per ADO org"],
]
add_table(s, Inches(0.4), Inches(4.3), Inches(12.5), Inches(2.5),
          cap_data, col_widths=[5, 1.5, 6], font_size=11)

slide_footer(s, slide_num, slides_total)


# ---------- 5. Pre-requisites ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Pre-requisites", "Must be in place before Week 1 kick-off")

prereq_data = [
    ["#", "Category", "Pre-requisite"],
    ["1", "Commercial", "GHE Enterprise (EMU) contract signed and tenant provisioned"],
    ["2", "Commercial", "GHE seat count confirmed >= 500 active users"],
    ["3", "Commercial", "Decision: GitHub Advanced Security in or out of Phase 1"],
    ["4", "Identity", "MoJ Entra ID tenant admin available for SAML + SCIM in Weeks 3-4"],
    ["5", "Identity", "Identity mapping spreadsheet started (ADO user -> Entra UPN -> EMU)"],
    ["6", "Identity", "Service principal in Entra for SCIM provisioning to GHE"],
    ["7", "Source-side", "Project Collection Admin access on every ADO org"],
    ["8", "Source-side", "PAT issued for migration service identity"],
    ["9", "Source-side", "Inventory of 100 repos with owner, BU, size, PR counts, integrations"],
    ["10", "Source-side", "Approval to install Azure Boards GitHub App at ADO org level"],
    ["11", "Target-side", "Target GHE orgs pre-created (1:1 with ADO orgs)"],
    ["12", "Target-side", "Baseline ruleset JSON template approved"],
    ["13", "Tooling", "GitHub CLI + gh-gei + gh-ado2gh installed on migration workstation"],
    ["14", "Tooling", "Azure Key Vault (or equivalent) for migration secrets"],
    ["15", "Network", "Outbound HTTPS to *.github.com permitted (proxy whitelist updated)"],
    ["16", "Governance", "Sponsor + steering committee + RAID log live"],
    ["17", "Governance", "Pilot wave volunteers confirmed (3-5 repos, low-risk)"],
    ["18", "Pipelines", "Azure Pipelines GitHub App install approved on GHE org(s)"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.85),
          prereq_data, col_widths=[0.5, 1.5, 8.5], font_size=10)

slide_footer(s, slide_num, slides_total)


# ---------- 6. Duration & Timeline ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Duration & Timeline", "10 calendar weeks across 5 stages with 5 milestones")

# Gantt
gx0 = Inches(2.5)
gx_w = Inches(10.3)
gy0 = Inches(1.4)
gantt_rows = [
    ("S0 Mobilise & Discovery", 0, 2, NAVY),
    ("S1 Identity & Foundation", 2, 4, TEAL),
    ("S2 Pilot Wave (5 repos)", 4, 6, AMBER),
    ("S3 Production Waves 1-4", 6, 9, GREEN),
    ("S4 Stabilisation & Close", 9, 10, RED),
]
row_h = Inches(0.55)
gap = Inches(0.1)
week_w = gx_w / 10.0

# Weeks header
for w in range(10):
    x = gx0 + week_w * w
    add_rect(s, x, gy0 - Inches(0.4), week_w, Inches(0.35), MGREY)
    add_text(s, x, gy0 - Inches(0.4), week_w, Inches(0.35),
             f"W{w+1}", size=10, bold=True, color=BLACK,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

for i, (label, start, end, color) in enumerate(gantt_rows):
    y = gy0 + i * (row_h + gap)
    # row label
    add_rect(s, Inches(0.4), y, Inches(2.0), row_h, LGREY)
    add_text(s, Inches(0.45), y, Inches(1.95), row_h,
             label, size=11, bold=True, color=NAVY,
             anchor=MSO_ANCHOR.MIDDLE)
    # bar
    bx = gx0 + week_w * start
    bw = week_w * (end - start)
    add_rect(s, bx, y + Inches(0.07), bw, row_h - Inches(0.14), color)

# Milestone diamonds
milestones = [
    ("M1", 2),
    ("M2", 4),
    ("M3", 6),
    ("M4", 9),
    ("M5", 10),
]
my = gy0 + 5 * (row_h + gap) + Inches(0.1)
for label, week in milestones:
    cx = gx0 + week_w * week - Inches(0.18)
    dia = s.shapes.add_shape(MSO_SHAPE.DIAMOND, cx, my, Inches(0.36), Inches(0.36))
    dia.fill.solid()
    dia.fill.fore_color.rgb = AMBER
    dia.line.color.rgb = BLACK
    dia.line.width = Pt(0.75)
    add_text(s, cx - Inches(0.4), my + Inches(0.4), Inches(1.0), Inches(0.3),
             label, size=10, bold=True, color=NAVY,
             align=PP_ALIGN.CENTER)

# Legend
legy = Inches(5.4)
add_text(s, Inches(0.4), legy, Inches(12), Inches(0.4),
         "Milestones", size=13, bold=True, color=NAVY)
ms_data = [
    ["#", "Milestone", "Exit Gate", "Week"],
    ["M1", "Mobilise & Discovery done", "Steering signs wave plan + risks", "End W2"],
    ["M2", "Identity Foundation live", "EMU + SAML + SCIM in production", "End W4"],
    ["M3", "Pilot Wave done", "5 repos live, Boards linked, pipelines re-pointed", "End W6"],
    ["M4", "Production Waves done", "100 repos in GHE, pipelines green", "End W9"],
    ["M5", "Phase 1 closed", "Hypercare exit, ADO archived, Phase 2 mandate", "End W10"],
]
add_table(s, Inches(0.4), Inches(5.85), Inches(12.5), Inches(1.2),
          ms_data, col_widths=[0.5, 3, 6.5, 1.5], font_size=10)

slide_footer(s, slide_num, slides_total)


# ---------- 7. Team & Resource Plan ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Team & Resource Plan", "8 people, ~5.3 peak FTE, ~150 person-days delivery effort")

team_data = [
    ["#", "Role", "Headcount", "FTE", "Weeks Active", "Person-days"],
    ["1", "Program Manager", "1", "0.5", "10", "25"],
    ["2", "Tech Lead / Architect", "1", "1.0", "10", "50"],
    ["3", "IAM Engineer", "1", "0.5 (front-loaded)", "10", "14"],
    ["4", "Platform / Migration Engineer #1", "1", "1.0", "8 (W3-W10)", "40"],
    ["5", "Platform / Migration Engineer #2", "1", "1.0", "8 (W3-W10)", "40"],
    ["6", "DevEx Engineer (pipelines)", "1", "0.7", "6 (W5-W10)", "21"],
    ["7", "InfoSec Engineer", "1", "0.3", "8 (W3-W10)", "12"],
    ["8", "Change Manager / Comms", "1", "0.3", "10", "15"],
    ["", "TOTAL", "8", "5.3 peak", "", "217 capacity / 150 effort"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(8.5), Inches(4.4),
          team_data, col_widths=[0.5, 3.5, 1.2, 1.8, 1.4, 1.6], font_size=11)

# Side note
add_rect(s, Inches(9.2), Inches(1.15), Inches(3.7), Inches(4.4), LGREY)
add_rect(s, Inches(9.2), Inches(1.15), Inches(3.7), Inches(0.45), TEAL)
add_text(s, Inches(9.2), Inches(1.15), Inches(3.7), Inches(0.45),
         "Capacity vs Effort", size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(9.35), Inches(1.7), Inches(3.5), Inches(3.7),
         ["150 p-days = billable",
          "value-added effort.",
          "",
          "217 p-days = nominal team",
          "capacity (8 ppl x weeks x FTE).",
          "",
          "Gap = ~67 p-days of",
          "realistic slack: meetings,",
          "handovers, waiting on deps,",
          "hypercare standby.",
          "",
          "Implies ~65-70% utilisation,",
          "which is normal for change-",
          "heavy programs."],
         size=11, color=BLACK)

# Roles outside the 8
add_rect(s, Inches(0.4), Inches(5.75), Inches(12.5), Inches(1.3), LGREY)
add_text(s, Inches(0.55), Inches(5.8), Inches(12.2), Inches(0.3),
         "Available on-demand (NOT on delivery headcount)", size=12, bold=True, color=NAVY)
add_text(s, Inches(0.55), Inches(6.1), Inches(12.2), Inches(0.9),
         ["- Sponsor (steering chair)   - MoJ ADO Project Collection Admins   - Repo Owners (~100, smoke-test sign-off)",
          "- Application SMEs / process owners   - Procurement / Licensing   - IT Ops (CMDB updates at archive)"],
         size=11, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 8. Resource Heatmap ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Resource Heatmap", "Effort intensity by role across the five stages")

heat = [
    ("Program Manager", ["N", "N", "N", "N", "N"]),
    ("Tech Lead / Architect", ["N", "N", "N", "N", "L"]),
    ("IAM Engineer",      ["L", "P", "L", "L", "O"]),
    ("Platform Eng x2",   ["L", "N", "P", "P", "L"]),
    ("DevEx Engineer",    ["O", "L", "P", "P", "L"]),
    ("InfoSec Engineer",  ["L", "L", "N", "N", "N"]),
    ("Change Manager",    ["P", "L", "N", "N", "L"]),
]
stages = ["S0 Mobilise", "S1 Foundation", "S2 Pilot", "S3 Waves", "S4 Close"]
color_map = {"P": RED, "N": GREEN, "L": AMBER, "O": MGREY}
label_map = {"P": "Peak", "N": "Normal", "L": "Light", "O": "Off"}

hx0 = Inches(2.7)
hy0 = Inches(1.4)
cell_w = Inches(1.9)
cell_h = Inches(0.55)

# Header row
for j, stg in enumerate(stages):
    x = hx0 + j * cell_w
    add_rect(s, x, hy0, cell_w, Inches(0.5), NAVY)
    add_text(s, x, hy0, cell_w, Inches(0.5),
             stg, size=11, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Rows
for i, (role, vals) in enumerate(heat):
    y = hy0 + Inches(0.5) + i * cell_h
    add_rect(s, Inches(0.4), y, Inches(2.3), cell_h, LGREY)
    add_text(s, Inches(0.45), y, Inches(2.25), cell_h,
             role, size=11, bold=True, color=NAVY,
             anchor=MSO_ANCHOR.MIDDLE)
    for j, v in enumerate(vals):
        x = hx0 + j * cell_w
        add_rect(s, x, y, cell_w, cell_h, color_map[v])
        add_text(s, x, y, cell_w, cell_h,
                 label_map[v], size=10, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Legend
lgy = Inches(5.5)
add_text(s, Inches(0.4), lgy, Inches(12), Inches(0.3),
         "Legend", size=12, bold=True, color=NAVY)
keys = [("Peak", RED), ("Normal", GREEN), ("Light", AMBER), ("Off", MGREY)]
for i, (k, c) in enumerate(keys):
    add_rect(s, Inches(0.4) + i * Inches(1.4), lgy + Inches(0.4), Inches(0.4), Inches(0.3), c)
    add_text(s, Inches(0.85) + i * Inches(1.4), lgy + Inches(0.4), Inches(1.0), Inches(0.3),
             k, size=11, color=BLACK, anchor=MSO_ANCHOR.MIDDLE)

# Risk note
add_rect(s, Inches(0.4), Inches(6.3), Inches(12.5), Inches(0.7), AMBER)
add_text(s, Inches(0.55), Inches(6.3), Inches(12.2), Inches(0.7),
         "Critical: IAM Engineer is the single biggest schedule risk. SAML + SCIM peak is Weeks 3-4. Book MoJ IAM resource at Week 1 and have a backup.",
         size=11, bold=True, color=BLACK, anchor=MSO_ANCHOR.MIDDLE)

slide_footer(s, slide_num, slides_total)


# ---------- 9. Effort by Workstream ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Effort Breakdown by Workstream", "150 person-days across 11 workstreams")

ws_data = [
    ["#", "Workstream", "Effort (p-days)", "% of Total"],
    ["WS1",  "Program Management & PMO",            "25",  "17%"],
    ["WS2",  "Identity & Access (EMU + SAML + SCIM)", "14",  "9%"],
    ["WS3",  "Platform / Migration Factory",         "10",  "7%"],
    ["WS4",  "Repo Migration (Pilot + 4 waves)",     "25",  "17%"],
    ["WS5",  "Azure Boards GitHub App Integration",  "4",   "3%"],
    ["WS6",  "Pipeline Source Re-pointing",          "20",  "13%"],
    ["WS7",  "Security, Policy & Rulesets",          "7",   "5%"],
    ["WS8",  "Comms & Training",                     "15",  "10%"],
    ["WS9",  "Decommission Prep (read-only freeze)", "5",   "3%"],
    ["WS10", "Hypercare (x5 waves)",                 "15",  "10%"],
    ["WS11", "Contingency (10%)",                    "10",  "7%"],
    ["",     "TOTAL",                                "150", "100%"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(8.0), Inches(5.0),
          ws_data, col_widths=[0.7, 5, 1.2, 1.1], font_size=11)

# Side panel - top efforts
add_rect(s, Inches(8.7), Inches(1.15), Inches(4.2), Inches(5.0), LGREY)
add_rect(s, Inches(8.7), Inches(1.15), Inches(4.2), Inches(0.45), NAVY)
add_text(s, Inches(8.7), Inches(1.15), Inches(4.2), Inches(0.45),
         "Top Effort Drivers", size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.85), Inches(1.7), Inches(4.0), Inches(4.3),
         ["1. PMO + Repo Migration (25 p-days each)",
          "   Largest cost centres",
          "",
          "2. Pipeline Re-pointing (20 p-days)",
          "   Higher if Classic-pipeline heavy",
          "",
          "3. Comms & Training (15 p-days)",
          "   Underestimating this is the #1",
          "   reason large migrations slip",
          "",
          "4. Hypercare (15 p-days)",
          "   Cap concurrent waves at 2",
          "",
          "5. IAM (14 p-days)",
          "   Critical path -- highest schedule",
          "   risk despite lower effort"],
         size=11, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 10. L1 Plan ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "L1 Plan - Milestones", "Five sequential stages with explicit exit gates")

l1_data = [
    ["#", "Milestone", "Exit Gate", "Calendar Week"],
    ["M1", "Mobilise & Discovery complete",
            "Steering sign-off on scope, wave plan, risk register",  "End of Week 2"],
    ["M2", "Identity Foundation live",
            "EMU + SAML + SCIM in production, >=95% users provisionable", "End of Week 4"],
    ["M3", "Pilot Wave complete",
            "5 repos migrated, Boards link verified, pipelines re-pointed, retrospective signed off", "End of Week 6"],
    ["M4", "Production Waves complete",
            "All 100 repos in GHE, all in-scope pipelines re-pointed and green", "End of Week 9"],
    ["M5", "Phase 1 closed",
            "Hypercare exited, ADO repos archived, lessons logged, Phase 2 mandate decision taken", "End of Week 10"],
]
add_table(s, Inches(0.4), Inches(1.2), Inches(12.5), Inches(2.8),
          l1_data, col_widths=[0.5, 3, 7, 1.5], font_size=11)

add_text(s, Inches(0.4), Inches(4.1), Inches(12.5), Inches(0.4),
         "Critical Path", size=14, bold=True, color=NAVY)

path = ["Sponsor sign-off", "Discovery & inventory", "Identity foundation",
        "Factory smoke test", "Pilot wave", "M3 gate", "Waves 1-4 (overlap)", "M5 close"]
gap = Inches(0.05)
bw = (SLIDE_W - Inches(0.8) - gap * (len(path) - 1)) / len(path)
py = Inches(4.6)
for i, p in enumerate(path):
    x = Inches(0.4) + i * (bw + gap)
    fill = NAVY if i == 0 or i == len(path) - 1 else TEAL
    add_rect(s, x, py, bw, Inches(0.9), fill)
    add_text(s, x, py, bw, Inches(0.9),
             p, size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Bottom note
add_rect(s, Inches(0.4), Inches(5.9), Inches(12.5), Inches(1.1), LGREY)
add_text(s, Inches(0.55), Inches(5.95), Inches(12.2), Inches(0.3),
         "Critical Path Risk", size=11, bold=True, color=RED)
add_text(s, Inches(0.55), Inches(6.25), Inches(12.2), Inches(0.7),
         ["The identity foundation (M2) is the longest-pole dependency.",
          "Any delay in MoJ Entra ID admin availability for SAML / SCIM will slip the whole program 1:1.",
          "Mitigation: book MoJ IAM resource in Week 1 and front-load the SCIM dry-run."],
         size=11, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 11. L2 Plan - Workstream Activities (S0+S1) ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "L2 Plan - Workstream Activities", "Stages 0 & 1: Mobilise, Discovery, Identity, Foundation")

# Two columns side by side
col_y = Inches(1.2)

# S0
add_rect(s, Inches(0.4), col_y, Inches(6.2), Inches(0.45), NAVY)
add_text(s, Inches(0.4), col_y, Inches(6.2), Inches(0.45),
         "Stage 0 - Mobilise & Discovery  (W1-2, ~20 p-days)",
         size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
s0_data = [
    ["Activity", "Owner", "Days"],
    ["Charter, RACI, steering setup", "PM", "2"],
    ["RAID log & first review", "PM", "1"],
    ["Comms plan, templates, distribution lists", "Change", "3"],
    ["Identity mapping CSV (ADO -> Entra UPN)", "IAM", "3"],
    ["Inventory all 100 repos", "Platform", "3"],
    ["Inventory all pipelines per repo", "DevEx", "2"],
    ["Inventory ADO branch policies per repo", "Platform", "2"],
    ["Baseline ruleset JSON definition", "InfoSec", "2"],
    ["Wave assignment (Pilot + 4 waves)", "Tech Lead", "2"],
]
add_table(s, Inches(0.4), col_y + Inches(0.5), Inches(6.2), Inches(4.0),
          s0_data, col_widths=[4.7, 1, 0.5], font_size=10)

# S1
add_rect(s, Inches(6.8), col_y, Inches(6.2), Inches(0.45), TEAL)
add_text(s, Inches(6.8), col_y, Inches(6.2), Inches(0.45),
         "Stage 1 - Identity & Foundation  (W3-4, ~22 p-days)",
         size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
s1_data = [
    ["Activity", "Owner", "Days"],
    ["EMU enterprise shell configuration", "IAM", "2"],
    ["SAML SSO with MoJ Entra ID", "IAM", "3"],
    ["SCIM provisioning Entra -> GHE", "IAM", "3"],
    ["Identity UAT with 10 test users", "IAM+TL", "2"],
    ["Migration factory: parameterised GEI scripts", "Platform", "3"],
    ["Secret vaulting (PATs in Key Vault)", "Platform", "1"],
    ["Migration tracking dashboard", "Platform", "2"],
    ["Sandbox GHE org for dry-runs", "Platform", "1"],
    ["Ruleset application script", "InfoSec", "1"],
    ["Comms templates finalised", "Change", "2"],
]
add_table(s, Inches(6.8), col_y + Inches(0.5), Inches(6.2), Inches(4.0),
          s1_data, col_widths=[4.7, 1, 0.5], font_size=10)

# Bottom note
add_rect(s, Inches(0.4), Inches(6.0), Inches(12.5), Inches(1.0), LGREY)
add_text(s, Inches(0.55), Inches(6.05), Inches(12.2), Inches(0.3),
         "Stage Exit Gates", size=11, bold=True, color=NAVY)
add_text(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.65),
         ["M1 (W2):  Steering signs off scope, wave plan, and risk register.",
          "M2 (W4):  EMU + SAML + SCIM in production. End-to-end factory smoke test passes against a throwaway repo."],
         size=11, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 12. L2 Plan - S2 Pilot ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "L2 Plan - Pilot Wave (Stage 2)", "Weeks 5-6: 5 low-risk repos, end-to-end validation")

pilot_data = [
    ["Activity", "Owner", "Days"],
    ["Pilot wave kickoff & comms", "PM + Change", "1"],
    ["Dry-run pilot migration in sandbox", "Migration Pod", "1"],
    ["Pilot Go/No-Go meeting", "Steering", "0.5"],
    ["Freeze pilot ADO repos (read-only)", "ADO Admin", "0.5"],
    ["Execute pilot migration (5 repos)", "Migration Pod", "1"],
    ["Apply rulesets + CODEOWNERS to pilot repos", "InfoSec + Platform", "1"],
    ["Install Azure Boards GitHub App on GHE pilot org", "Platform + ADO Admin", "0.5"],
    ["Connect Boards App to ADO org/projects", "Platform + ADO Admin", "0.5"],
    ["Test AB#123 linking (commits, PRs, branches, merge)", "DevEx + Owners", "1"],
    ["Install Azure Pipelines GitHub App on GHE org", "Platform", "0.5"],
    ["Re-point pilot pipelines (5-10 pipelines)", "DevEx", "2"],
    ["Validate build + release end-to-end", "DevEx + Owners", "1"],
    ["Mannequin reclamation for pilot", "Platform", "1"],
    ["Hypercare D+1 -> D+3", "Wave Lead + Pods", "2"],
    ["Archive pilot ADO repos (D+7)", "ADO Admin", "0.5"],
    ["Pilot retrospective + runsheet update", "PM", "1"],
    ["M3 gate: pilot accepted, scale authorised", "Steering", "0.5"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.5),
          pilot_data, col_widths=[7.5, 4, 1], font_size=10)

# Pilot KPI
add_rect(s, Inches(0.4), Inches(6.75), Inches(12.5), Inches(0.35), AMBER)
add_text(s, Inches(0.55), Inches(6.75), Inches(12.2), Inches(0.35),
         "Pilot exits cleanly when: 5 repos live, Boards links verified, pipelines green, zero P1/P2 defects open, retrospective signed off.",
         size=10, bold=True, color=BLACK, anchor=MSO_ANCHOR.MIDDLE)

slide_footer(s, slide_num, slides_total)


# ---------- 13. L2 Plan - S3 Waves ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "L2 Plan - Production Waves (Stage 3)", "Weeks 7-9: 4 waves of ~25 repos each, 2 in flight at a time")

# Per-wave template
add_text(s, Inches(0.4), Inches(1.2), Inches(12), Inches(0.4),
         "Per-Wave Template (~11 p-days, repeated 4x)",
         size=14, bold=True, color=NAVY)
wave_data = [
    ["#", "Activity", "Owner", "Days"],
    ["1",  "Wave manifest confirmed (repos, owners, pipelines)", "Wave Lead", "0.5"],
    ["2",  "T-10 / T-3 / T-1 comms", "Change Mgr", "1"],
    ["3",  "Dry-run wave migration in sandbox", "Migration Pod", "1"],
    ["4",  "Go / No-Go meeting", "Steering", "0.5"],
    ["5",  "Freeze wave ADO repos", "ADO Admin", "0.5"],
    ["6",  "Execute migration (25 repos in parallel)", "Migration Pod", "1"],
    ["7",  "Apply rulesets + CODEOWNERS", "InfoSec + Platform", "0.5"],
    ["8",  "Verify Boards integration on new repos", "DevEx", "0.5"],
    ["9",  "Re-point pipelines for wave (~25-50 pipelines)", "DevEx", "3"],
    ["10", "Validate builds for wave", "DevEx + Owners", "1"],
    ["11", "Mannequin reclamation", "Platform", "1"],
    ["12", "Hypercare D+1 -> D+3", "Wave Lead + Pods", "2"],
    ["13", "Archive wave ADO repos (D+7)", "ADO Admin", "0.5"],
]
add_table(s, Inches(0.4), Inches(1.7), Inches(8.5), Inches(4.7),
          wave_data, col_widths=[0.4, 5.2, 2, 0.7], font_size=10)

# Side - concurrency model
add_rect(s, Inches(9.2), Inches(1.7), Inches(3.7), Inches(4.7), LGREY)
add_rect(s, Inches(9.2), Inches(1.7), Inches(3.7), Inches(0.45), TEAL)
add_text(s, Inches(9.2), Inches(1.7), Inches(3.7), Inches(0.45),
         "Wave Cadence", size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(9.35), Inches(2.25), Inches(3.5), Inches(4.1),
         ["W7  W8  W9",
          "",
          "[--W1--]",
          "    [--W2--]",
          "        [--W3--]",
          "            [--W4--]",
          "",
          "Max 2 waves in flight.",
          "",
          "No new wave starts",
          "during another wave's",
          "D-0 -> D+3 window.",
          "",
          "4 x 25 = 100 repos",
          "all live by end W9."],
         size=11, color=BLACK)

# Bottom strip
add_rect(s, Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.55), NAVY)
add_text(s, Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.55),
         "Total Stage 3 effort: ~44 p-days   |   Calendar duration: 3 weeks   |   M4 gate: 100 repos in GHE, pipelines green",
         size=11, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

slide_footer(s, slide_num, slides_total)


# ---------- 14. L3 sample ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "L3 Plan - Detailed Task Sample", "Stage 0 task breakdown (full L3 covers ~80 numbered tasks)")

l3_data = [
    ["ID", "Task", "Owner", "Days", "Predecessors"],
    ["0.1",  "Sponsor sign-off & charter", "PM", "1", "-"],
    ["0.2",  "RACI agreed", "PM", "0.5", "0.1"],
    ["0.3",  "Steering committee chartered, first meeting", "PM", "0.5", "0.1"],
    ["0.4",  "RAID log v1 published", "PM", "1", "0.1"],
    ["0.5",  "Comms plan signed off", "Change Mgr", "2", "0.1"],
    ["0.6",  "Stakeholder & contact matrix (per repo)", "Change Mgr", "1", "0.1"],
    ["0.7",  "Pull ADO users from all 100 repos", "IAM", "1", "0.1"],
    ["0.8",  "Identity mapping CSV (ADO/Entra/EMU)", "IAM", "2", "0.7"],
    ["0.9",  "Inventory: gh ado2gh inventory-report", "Platform", "1", "0.1"],
    ["0.10", "Repo size + LFS audit", "Platform", "1", "0.9"],
    ["0.11", "Open PRs + open branches snapshot", "Platform", "1", "0.9"],
    ["0.12", "Pipeline inventory per repo (YAML vs Classic)", "DevEx", "2", "0.9"],
    ["0.13", "ADO branch policy inventory per repo", "Platform", "2", "0.9"],
    ["0.14", "ADO service connections inventory", "DevEx", "1", "0.9"],
    ["0.15", "Complexity scoring per repo", "Tech Lead", "1", "0.10-0.14"],
    ["0.16", "Wave assignment (Pilot + W1-W4)", "Tech Lead", "1", "0.15"],
    ["0.17", "Baseline ruleset JSON v1", "InfoSec", "2", "0.13"],
    ["0.18", "CODEOWNERS template", "Platform", "0.5", "-"],
    ["0.19", "M1 gate: sign-off on wave plan & risks", "PM + Sponsor", "0.5", "0.16, 0.17"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.5),
          l3_data, col_widths=[0.6, 6, 1.5, 0.6, 1.3], font_size=10)

add_rect(s, Inches(0.4), Inches(6.75), Inches(12.5), Inches(0.35), AMBER)
add_text(s, Inches(0.55), Inches(6.75), Inches(12.2), Inches(0.35),
         "Full L3 covers ~80 tasks across all 5 stages. Available as CSV / project plan on request.",
         size=10, bold=True, color=BLACK, anchor=MSO_ANCHOR.MIDDLE)

slide_footer(s, slide_num, slides_total)


# ---------- 15. Risks ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Phase 1 Risks & Mitigations", "Top 10 risks ranked")

risk_data = [
    ["#", "Risk", "L", "I", "Mitigation"],
    ["R1", "Entra SAML / SCIM delayed (MoJ admin availability)", "Med", "High", "Book MoJ IAM in W1; backup admin"],
    ["R2", "Pipeline re-point harder than expected (Classic %)", "Med", "High", "Inventory Classic % early; +20% buffer"],
    ["R3", "Branch policies don't map perfectly to rulesets", "Low", "Med", "Baseline ruleset + per-repo exceptions list"],
    ["R4", "Mannequin reclamation gaps (ex-staff)", "High", "Low", "Define unreclaimed-mannequin policy"],
    ["R5", "LFS / oversize repos exceed GHE limits", "Low", "High", "Audit in Stage 0; remediate before wave assignment"],
    ["R6", "Hardcoded ADO URLs in IaC / pipelines / docs", "Med", "Med", "Inventory in Stage 0; redirect map; comms"],
    ["R7", "Boards App rate limits across 100 repos", "Low", "Med", "Stagger app install; monitor"],
    ["R8", "Concurrent waves overload hypercare team", "Med", "Med", "Hard cap 2 waves concurrent"],
    ["R9", "Repo owners not available for smoke tests", "Med", "Med", "Confirm at T-10; escalation path"],
    ["R10", "Pipeline secrets recreation gaps", "Med", "High", "Secret inventory per pipeline; checklist"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.9),
          risk_data, col_widths=[0.5, 5.5, 0.8, 0.8, 4.9], font_size=10)

slide_footer(s, slide_num, slides_total)


# ---------- 16. Decisions Needed ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Decisions Required at Mobilise", "Steering must close these in Week 1")

dec_data = [
    ["#", "Decision", "Recommendation", "Owner"],
    ["D1", "Pilot wave repos (5)", "Low-risk, willing teams, mix of YAML + Classic pipelines", "Steering"],
    ["D2", "GHAS in scope for Phase 1?", "YES - code scanning + secret scanning + Dependabot baseline", "InfoSec + Sponsor"],
    ["D3", "Disable GitHub Issues per repo?", "YES - Boards stays in ADO; avoid drift", "Steering"],
    ["D4", "Mannequin policy for ex-staff", "Leave unreclaimed after 30 days; attribute to bot account", "InfoSec + IAM"],
    ["D5", "Auto-state-transition rules per work item type", "Use ADO defaults; document per project", "Apps SMEs"],
    ["D6", "ADO retention window post-archive", "90 days read-only, then delete", "Sponsor + InfoSec"],
    ["D7", "Concurrent wave cap", "2 waves max in flight", "Steering"],
    ["D8", "Backup IAM resource for SAML / SCIM peak", "Identify named backup before Week 3", "Sponsor"],
    ["D9", "Hypercare on-call rota across waves", "Dedicated rota; no double-booking with delivery work", "PM"],
    ["D10", "Branch protection enforcement on day one?", "YES - block non-compliant pushes from cutover", "InfoSec"],
]
add_table(s, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.85),
          dec_data, col_widths=[0.5, 4.5, 5.5, 2], font_size=10)

slide_footer(s, slide_num, slides_total)


# ---------- 17. Phase 2 Preview ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Phase 2 Preview (Not in this estimate)",
             "Migrate CI/CD to GitHub Actions after Phase 1 close")

# Scope box
add_rect(s, Inches(0.4), Inches(1.2), Inches(6.2), Inches(3.0), LGREY)
add_rect(s, Inches(0.4), Inches(1.2), Inches(6.2), Inches(0.45), NAVY)
add_text(s, Inches(0.4), Inches(1.2), Inches(6.2), Inches(0.45),
         "Phase 2 Scope", size=13, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(1.8), Inches(6), Inches(2.3),
         ["- Convert Azure Pipelines -> GitHub Actions",
          "  workflows (use gh actions-importer)",
          "",
          "- Re-platform Release pipelines to GitHub",
          "  Actions Environments + approvals + gates",
          "",
          "- Stand up self-hosted runners on Azure VMSS",
          "",
          "- OIDC federation to Azure subscriptions",
          "  (eliminate service-connection secrets)",
          "",
          "- Decommission Azure Pipelines / Releases"],
         size=11, color=BLACK)

# Effort box
add_rect(s, Inches(6.8), Inches(1.2), Inches(6.2), Inches(3.0), LGREY)
add_rect(s, Inches(6.8), Inches(1.2), Inches(6.2), Inches(0.45), TEAL)
add_text(s, Inches(6.8), Inches(1.2), Inches(6.2), Inches(0.45),
         "Indicative Effort", size=13, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
p2_data = [
    ["Theme", "Effort"],
    ["Actions Importer setup & audit", "5 p-days"],
    ["Self-hosted runners (VMSS)", "8 p-days"],
    ["OIDC federation to Azure", "3 p-days"],
    ["Pipeline conversion (avg per pipeline)", "0.5-2 p-days"],
    ["Release pipeline conversion (per release)", "1-3 p-days"],
    ["Hypercare + cutover per wave", "3 p-days"],
]
add_table(s, Inches(6.95), Inches(1.75), Inches(5.9), Inches(2.3),
          p2_data, col_widths=[4.5, 1.4], font_size=11)

# Headline
add_rect(s, Inches(0.4), Inches(4.5), Inches(12.5), Inches(1.0), AMBER)
add_text(s, Inches(0.4), Inches(4.5), Inches(12.5), Inches(1.0),
         "Indicative Phase 2 duration: 12-16 weeks   |   Effort: 200-250 person-days",
         size=20, bold=True, color=BLACK,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Detail note
add_rect(s, Inches(0.4), Inches(5.7), Inches(12.5), Inches(1.4), LGREY)
add_text(s, Inches(0.55), Inches(5.75), Inches(12.2), Inches(0.3),
         "Note", size=12, bold=True, color=NAVY)
add_text(s, Inches(0.55), Inches(6.05), Inches(12.2), Inches(1.0),
         ["A detailed Phase 2 estimate should be produced at Phase 1 close (M5)",
          "when actual pipeline counts, Classic vs YAML ratio, and per-environment release complexity are known.",
          "Phase 2 is dependent on a successful Phase 1 hypercare exit -- it is not initiated in parallel."],
         size=11, color=BLACK)

slide_footer(s, slide_num, slides_total)


# ---------- 18. Next Steps ----------
slide_num += 1
s = prs.slides.add_slide(BLANK)
slide_header(s, "Next Steps", "Decisions and actions to authorise Week 1")

steps = [
    ("1", "Confirm Phase 1 scope and approach",
        "Steering signs off this deck. Locks the hybrid model: code in GHE, work items + releases in ADO."),
    ("2", "Close the 10 mobilise decisions (D1-D10)",
        "Especially: pilot 5 repos, GHAS in/out, mannequin policy, backup IAM resource."),
    ("3", "Confirm GHE Enterprise (EMU) procurement and tenant",
        "Procurement and licensing in place before Week 1."),
    ("4", "Confirm team composition (8 roles)",
        "Named individuals across PM, Tech Lead, IAM, 2x Platform, DevEx, InfoSec, Change."),
    ("5", "Book MoJ Entra ID admin for SAML + SCIM in Weeks 3-4",
        "Highest-risk dependency. Must be booked at kick-off, not later."),
    ("6", "Issue ADO PAT for migration service identity and vault it",
        "Required by Platform team in Week 2 for inventory + dry-runs."),
    ("7", "Kick off Stage 0 - Mobilise & Discovery",
        "Week 1 starts. Inventory of 100 repos begins. M1 gate at end of Week 2."),
]
for i, (n, title, desc) in enumerate(steps):
    y = Inches(1.2) + i * Inches(0.75)
    add_rect(s, Inches(0.4), y, Inches(0.6), Inches(0.7), NAVY)
    add_text(s, Inches(0.4), y, Inches(0.6), Inches(0.7),
             n, size=20, bold=True, color=AMBER,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(1.05), y, Inches(11.85), Inches(0.7), LGREY)
    add_text(s, Inches(1.2), y + Inches(0.05), Inches(11.6), Inches(0.3),
             title, size=12, bold=True, color=NAVY)
    add_text(s, Inches(1.2), y + Inches(0.35), Inches(11.6), Inches(0.35),
             desc, size=10, color=BLACK)

slide_footer(s, slide_num, slides_total)


# Attach speaker notes to each slide
for idx, slide in enumerate(prs.slides, start=1):
    note = SPEAKER_NOTES.get(idx, "")
    if note:
        slide.notes_slide.notes_text_frame.text = note

# Save
out = r"C:\Users\nazmohammed\.copilot\session-state\f7603c23-d320-431c-874f-087287e33674\files\ADO-to-GHE-Phase1-Plan.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
print(f"Speaker notes attached: {sum(1 for _ in SPEAKER_NOTES)}")
