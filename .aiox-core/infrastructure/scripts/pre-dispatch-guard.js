'use strict';

/**
 * CLI bridge for the AIOX pre-dispatch governance contract.
 *
 * This file is intentionally small: the source of truth remains
 * `.aiox-core/core/permissions/dispatch-governance.js`. The bridge translates
 * environment/context input used by pm.sh into that shared contract.
 */

const fs = require('fs');
const path = require('path');
const {
  DispatchGovernanceError,
  assertDispatchGovernance,
} = require('../../core/permissions/dispatch-governance');

/**
 * Load and validate a JSON dispatch context file.
 * @param {string|undefined} filePath - Context file path.
 * @returns {object} Parsed context object, or an empty object when omitted.
 * @throws {Error} When the file is missing, invalid, or not an object.
 */
function loadContext(filePath) {
  if (!filePath) return {};
  const resolved = path.resolve(filePath);
  if (!fs.existsSync(resolved)) {
    throw new Error(`Dispatch context file not found: ${resolved}`);
  }
  const parsed = JSON.parse(fs.readFileSync(resolved, 'utf8'));
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error('Dispatch context must be a JSON object.');
  }
  return parsed;
}

function buildOptions(env = process.env) {
  const context = loadContext(env.AIOX_DISPATCH_CONTEXT);
  const contextIntent = [
    context.instructions,
    context.prompt,
    context.intent,
  ].filter(Boolean).join('\n');
  const params = env.AIOX_DISPATCH_PARAMS || '';
  return {
    budgetCeilingUsd: env.AIOX_MODEL_BUDGET_CEILING_USD,
    task: env.AIOX_DISPATCH_TASK || '',
    intent: [params, contextIntent].filter(Boolean).join('\n'),
    story: context.story || context.storyPath || context.storyId,
    projectRoot: env.AIOX_PROJECT_ROOT || process.cwd(),
  };
}

/**
 * Execute the shared AIOX dispatch governance contract.
 * @param {object} options - Governance options.
 * @returns {{ok: boolean, evidence?: object, error?: object}} Guard result.
 */
function run(options = {}) {
  try {
    const evidence = assertDispatchGovernance(options);
    return { ok: true, evidence };
  } catch (error) {
    if (error instanceof DispatchGovernanceError) {
      return {
        ok: false,
        error: {
          code: error.code,
          message: error.message,
          details: error.details,
        },
      };
    }
    return {
      ok: false,
      error: {
        code: 'DISPATCH_GUARD_ERROR',
        message: error.message,
        details: {},
      },
    };
  }
}

/**
 * Run the guard from process environment variables.
 * @param {NodeJS.ProcessEnv} [env] - Environment values to translate.
 * @returns {number} Process-compatible exit code: 0 for allow, 5 for reject.
 */
function main(env = process.env) {
  const result = run(buildOptions(env));
  if (!result.ok) {
    process.stderr.write(`${result.error.code}: ${result.error.message}\n`);
    return 5;
  }
  return 0;
}

if (require.main === module) {
  process.exitCode = main();
}

module.exports = {
  loadContext,
  buildOptions,
  run,
  main,
};
